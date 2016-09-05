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

from openerp import models


class ProjectCompassion(models.Model):
    _inherit = 'compassion.project'

    def _hold_letters(self):
        letters = self.env['correspondence'].search([
            ('child_id.local_id', 'like', self.icp_id),
            ('direction', '=', 'Supporter To Beneficiary'),
            ('kit_identifier', '=', False),
            ('state', '=', 'Received in the system'),
        ])
        letters.hold_letters()

    def _reactivate_letters(self):
        letters = self.env['correspondence'].search([
            ('child_id.local_id', 'like', self.icp_id),
            ('direction', '=', 'Supporter To Beneficiary'),
            ('kit_identifier', '=', False),
            ('state', '=', 'Received in the system'),
        ])
        letters.reactivate_letters()
