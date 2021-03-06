# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 Compassion CH (http://www.compassion.ch)
#    Releasing children from poverty in Jesus' name
#    @author: Emanuel Cino
#
#    The licence is in the file __openerp__.py
#
##############################################################################
from openerp import models, api, fields, _
from openerp.exceptions import Warning


class ImportReview(models.TransientModel):
    """
    Browse through the import lines and allow the user to review and correct
    the results easily.
    """

    _name = 'import.letters.review'

    ##########################################################################
    #                                 FIELDS                                 #
    ##########################################################################
    progress = fields.Float(compute='_get_current_line', store=True)
    current_line_index = fields.Integer(default=0)
    count = fields.Integer(compute='_get_current_line', store=True)
    nb_lines = fields.Integer(compute='_get_current_line', store=True)
    current_line_id = fields.Many2one(
        'import.letter.line', 'Letter', compute='_get_current_line',
        store=True, readonly=True)
    postpone_import_id = fields.Many2one('import.letters.history')

    # Import line related fields
    state = fields.Selection(related='current_line_id.status', readonly=True)
    letter_image = fields.Binary(compute='_get_current_line')
    letter_file = fields.Binary(
        'Letter file', readonly=True, compute='_get_current_line')
    fname = fields.Char(related='current_line_id.letter_image.name')
    partner_id = fields.Many2one(related='current_line_id.partner_id')
    sponsorship_id = fields.Many2one('recurring.contract', 'Sponsorship')
    child_id = fields.Many2one(related='current_line_id.child_id')
    template_id = fields.Many2one(related='current_line_id.template_id')
    language_id = fields.Many2one(
        related='current_line_id.letter_language_id',
        order='translatable desc, id asc')
    is_encourager = fields.Boolean(related='current_line_id.is_encourager')
    mandatory_review = fields.Boolean(
        related='current_line_id.mandatory_review')
    physical_attachments = fields.Selection(
        related='current_line_id.physical_attachments')
    attachments_description = fields.Char(
        related='current_line_id.attachments_description')
    edit = fields.Boolean('Edit mode')

    ##########################################################################
    #                             FIELDS METHODS                             #
    ##########################################################################
    @api.one
    @api.depends('current_line_index')
    def _get_current_line(self):
        line_ids = self.env.context.get('line_ids')
        if line_ids:
            self.current_line_id = line_ids[self.current_line_index]
            self.nb_lines = len(line_ids)
            self.count = self.current_line_index + 1
            self.progress = (float(self.count) / self.nb_lines) * 100
            self.letter_image = self.with_context(
                bin_size=False).current_line_id.letter_image_preview
            self.letter_file = self.with_context(
                bin_size=False).current_line_id.letter_image.datas

    @api.onchange('sponsorship_id')
    def _get_partner_child(self):
        for wizard in self:
            child = wizard.sponsorship_id.child_id
            if child:
                wizard.child_id = child

    @api.onchange('partner_id')
    def _get_default_sponsorship(self):
        self.ensure_one()
        if self.partner_id:
            sponsorships = self.env['recurring.contract'].search([
                ('correspondant_id', '=', self.partner_id.id)
            ])
            if len(sponsorships) == 1:
                self.sponsorship_id = sponsorships

    ##########################################################################
    #                             VIEW CALLBACKS                             #
    ##########################################################################
    @api.multi
    def next(self):
        """ Load the next import line in the view. """
        self.ensure_one()
        if self.current_line_id.status not in ('ok', 'no_template'):
            raise Warning(
                _("Import is not valid"),
                _("Please review this import before going to the next."))
        self.write({
            'current_line_index': self.current_line_index + 1,
            'sponsorship_id': False,
        })
        self.current_line_id.reviewed = True

    @api.multi
    def finish(self):
        """ Return to import view. """
        self.ensure_one()
        import_history = self.current_line_id.import_id
        import_history.import_line_ids.check_status()
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form,tree',
            'res_model': import_history._name,
            'res_id': import_history.id,
            'context': self.env.context,
            'target': 'current',
        }

    @api.multi
    def postpone(self):
        """ Move the line in another import. """
        self.ensure_one()
        postpone_import = self.postpone_import_id
        current_import = self.current_line_id.import_id
        if not postpone_import:
            import_vals = current_import.get_correspondence_metadata()
            import_vals['import_completed'] = True
            postpone_import = self.env['import.letters.history'].create(
                import_vals)
            self.postpone_import_id = postpone_import
        self.current_line_id.import_id = postpone_import
        self.current_line_index += 1
