# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2016 Compassion CH (http://www.compassion.ch)
#    Releasing children from poverty in Jesus' name
#    @author: Emanuel Cino <ecino@compassion.ch>
#
#    The licence is in the file __openerp__.py
#
##############################################################################

from openerp import models, fields, api

from openerp.addons.child_compassion.models.compassion_hold import \
    HoldType


class EndContractWizard(models.TransientModel):
    _inherit = 'end.contract.wizard'

    child_id = fields.Many2one(related='contract_id.child_id')
    do_transfer = fields.Boolean('I want to transfer the child')
    transfer_country_id = fields.Many2one(
        'compassion.global.partner', 'Country')
    keep_child_on_hold = fields.Boolean(default=True)
    hold_expiration_date = fields.Datetime(
        default=lambda s: s.env[
            'compassion.hold'].get_default_hold_expiration(
            HoldType.SPONSOR_CANCEL_HOLD),
        required=True)

    @api.multi
    def end_contract(self):
        self.ensure_one()
        child = self.child_id

        if self.keep_child_on_hold:
            if child.hold_id:
                # Update the hold
                child.hold_id.write({
                    'type': HoldType.SPONSOR_CANCEL_HOLD.value,
                    'expiration_date': self.hold_expiration_date
                })
            else:
                # Setup a hold expiration in the sponsorship
                self.contract_id.hold_expiration_date = \
                    self.hold_expiration_date
        else:
            # Setup the hold expiration now
            self.contract_id.hold_expiration_date = fields.Datetime.now()
            # Remove the hold on the child
            if child.hold_id:
                child.hold_id.release_hold()

        child.signal_workflow('release')

        return super(EndContractWizard, self).end_contract()
