# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2016 Compassion CH (http://www.compassion.ch)
#    Releasing children from poverty in Jesus' name
#    @author: Emanuel Cino <ecino@compassion.ch>, Philippe Heer
#
#    The licence is in the file __openerp__.py
#
##############################################################################


from openerp import models, fields, api, _
from openerp.addons.message_center_compassion.mappings \
    import base_mapping as mapping


class ChildLifecycleEvent(models.Model):
    """ A child lifecycle event (BLE) """
    _name = 'compassion.child.ble'
    _description = 'Child Lifecycle Event'
    _inherit = 'translatable.model'
    _order = 'date desc, id desc'

    child_id = fields.Many2one(
        'compassion.child', 'Child', required=True, ondelete='cascade',
        readonly=True)
    global_id = fields.Char(readonly=True, required=True)
    date = fields.Datetime(readonly=True)
    type = fields.Selection([
        ('Planned Exit', 'Planned Exit'),
        ('Registration', 'Registration'),
        ('Reinstatement', 'Reinstatement'),
        ('Transfer', 'Transfer'),
        ('Transition', 'Transition'),
        ('Unplanned Exit', 'Unplanned Exit'),
    ], readonly=True)

    # All reasons for all request types
    request_reason = fields.Selection([
        # Child Registration
        ('Registration with Compassion', _('Child registration')),
        # Planned Exit
        ('Reached Maximum Age', _('{he} reached maximum age')),
        ('Reached the end of the relevant programs available at the church '
         'partner', _('{he} reached the end of the relevant programs '
                      'available')),
        ('Reached max age or completion date but did not fulfill '
         'completion plan',
         'Reached max age or completion date but did not fulfill '
         'completion plan'),
        ('Reached the end of relevant programs available at ICP',
         'Reached the end of relevant programs available at ICP'),
        # Reinstatement
        ('Beneficiary Exit was mistake', 'Exit was mistake'),
        ('Beneficiary Moved Back', 'Beneficiary Moved Back'),
        ('Family Needs Help Again', 'Family Needs Help Again'),
        ('No Longer Sponsored by Another Organization',
         'No Longer Sponsored by Another Organization'),
        ('Other (enter reason below)', 'Other'),
        ('Other (Enter Reason)', 'Other (Enter Reason)'),
        # Transfer
        ('Relocation: Caregiver\'s Work.', 'Relocation: Caregiver\'s Work.'),
        ('Relocation: Moved To Another Area',
         'Relocation: Moved To Another Area'),
        ('Relocation: Vocational/Technical Or Higher Education.',
         'Relocation: Vocational/Technical Or Higher Education.'),
        ('Programming Availability Is A Better Fit For Beneficiary',
         'Programming Availability Is A Better Fit For Beneficiary'),
        ('Project Closure', 'Project Closure'),
        ('Project Downsizing', 'Project Downsizing'),
        ('Special Needs', 'Special Needs'),
        ('Beneficiary/Caregiver moving to another location',
         'Beneficiary/Caregiver moving to another location'),
        # Unplanned Exit
        ('Child / Caregiver does not comply with policies',
         _('{he} does not comply with policies')),
        ('Child in system under two numbers (enter other number in the '
         'Comments box below)', _('{he} is in system under two numbers')),
        ('Child places others at risk', _('{he} places others at risk')),
        ('Child sponsored by another organization',
         _('{he} is sponsored by another organization')),
        ('Death of caregiver creates situation where child cannot continue',
         _('{his} caregiver died')),
        ('Death of child', '{he} passed away'),
        ('Family Circumstances Have Changed Positively So That Child No '
         'Longer Needs Compassion\'s Assistance',
         _('family circumstances have changed positively')),
        ('Family moved where a Compassion project with relevant programs is '
         'not available', _('{his} family moved where a Compassion project '
                            'with relevant programs is not available')),
        ('Project or program closure', _('of the project closure')),
        ('Taken out of project by parents, or family no longer interested '
         'in program', _('{he} was taken out of project by parents')),
        ('Unjustified absence from program activities for Greater Than 2 '
         'months', _('of an unjustified absence for greater than 2 months')),
        ('Child ran away', 'Child ran away'),
        ('Crisis', 'Crisis'),
        ('Deceased', 'Deceased'),
        ('Fulfilled completion plan and reached completion date',
         'Fulfilled completion plan and reached completion date'),
        ('Gone into military service', 'Gone into military service'),
        ('No longer interested in the Program', 'No longer interested in '
                                                'the Program'),
        ('Project Capacity Issue', 'Project Capacity Issue'),

    ], readonly=True)

    # Common fields
    ###############
    # comments = fields.Char(readonly=True)
    status = fields.Selection([
        ('Cancelled', 'Cancelled'),
        ('Closed', 'Closed'),
        ('In Progress', 'In Progress'),
        ('Open', 'Open'),
    ])

    # Planned Exit fields
    #####################
    last_attended_project = fields.Date(readonly=True)
    primary_school_finished = fields.Boolean(readonly=True)
    # confesses_jesus_savior = fields.Boolean(readonly=True)
    final_letter_sent = fields.Boolean(readonly=True)
    sponsor_impact = fields.Char(readonly=True)
    new_situation = fields.Char(readonly=True)
    future_hopes = fields.Char(readonly=True)
    family_impact = fields.Char(readonly=True)

    # Transfer fields
    #################
    old_project_id = fields.Many2one('compassion.project', readonly=True)
    transfer_arrival_date = fields.Date(readonly=True)
    other_transfer_reason = fields.Char(readonly=True)
    current_project = fields.Char(readonly=True)
    new_project = fields.Char(readonly=True)
    new_program = fields.Char(readonly=True)
    previously_active_program = fields.Char(readonly=True)

    # Transition fields
    ###################
    transition_type = fields.Selection([
        ('Sponsorship-Home to Sponsorship-Center', 'Home to Center'),
        ('Survival to Sponsorship-Home', 'Survival to Home'),
        ('Traditional Survival to Sponsorship-Center',
         'Traditional Survival to Center'),
    ], readonly=True)

    # Unplanned Exit fields
    #######################
    child_death_date = fields.Date(readonly=True)
    death_intervention_information = fields.Char(readonly=True)

    child_death_category = fields.Selection([
        ('Abuse', 'Abuse'),
        ('Fatal Accident or Suicide', 'Fatal Accident or Suicide'),
        ('Gastro-Intestinal', 'Gastro-Intestinal'),
        ('Infection', 'Infection'),
        ('Maternal', 'Maternal'),
        ('Neonatal Disorders', 'Neonatal Disorders'),
        ('Non-Communicable Diseases', 'Non-Communicable Diseases'),
        ('Respiratory-Related', 'Respiratory-Related'),
        ('Unknown Cause', 'Unknown Cause'),
        ('Vaccine-Preventable Diseases', 'Vaccine-Preventable Diseases'),
        ('Vector-Borne', 'Vector-Borne'),
    ], readonly=True)
    child_death_subcategory = fields.Selection([
        ('Abortion-related', 'Abortion-related'),
        ('Anemia', 'Anemia'),
        ('Asphyxia', 'Asphyxia'),
        ('Birth Asphyxia', 'Birth Asphyxia'),
        ('Bronchitis', 'Bronchitis'),
        ('Burns', 'Burns'),
        ('Cancer', 'Cancer'),
        ('Cardiovascular', 'Cardiovascular'),
        ('Chicken Pox', 'Chicken Pox'),
        ('Chikungunya', 'Chikungunya'),
        ('Cholera', 'Cholera'),
        ('Congenital Abnormalities', 'Congenital Abnormalities'),
        ('Dengue', 'Dengue'),
        ('Diabetes', 'Diabetes'),
        ('Diarrhea', 'Diarrhea'),
        ('Diphtheria', 'Diphtheria'),
        ('Drowning', 'Drowning'),
        ('Electrocution', 'Electrocution'),
        ('Epilepsy/Seizure Disorder', 'Epilepsy/Seizure Disorder'),
        ('Falls', 'Falls'),
        ('HIV/AIDS-related', 'HIV/AIDS-related'),
        ('Hepatitis', 'Hepatitis'),
        ('Influenza', 'Influenza'),
        ('Intra-partum-related Complications',
         'Intra-partum-related Complications'),
        ('Japanese Encephalitis', 'Japanese Encephalitis'),
        ('Leukemia', 'Leukemia'),
        ('Malaria', 'Malaria'),
        ('Measles', 'Measles'),
        ('Meningitis', 'Meningitis'),
        ('Mumps', 'Mumps'),
        ('Natural Disaster', 'Natural Disaster'),
        ('Obstructed Labor', 'Obstructed Labor'),
        ('Other', 'Other'),
        ('Parasites', 'Parasites'),
        ('Pertussis', 'Pertussis'),
        ('Physical', 'Physical'),
        ('Pneumonia', 'Pneumonia'),
        ('Poisoning', 'Poisoning'),
        ('Polio', 'Polio'),
        ('Postpartum Complications (Hemorrhage, infection etc.)',
         'Postpartum Complications (Hemorrhage, infection etc.)'),
        ('Pregnancy Complications (Preeclampsia, eclampsia, etc.)',
         'Pregnancy Complications (Preeclampsia, eclampsia, etc.)'),
        ('Prematurity/ Low Birth Weight', 'Prematurity/ Low Birth Weight'),
        ('Renal Disease', 'Renal Disease'),
        ('Respiratory Tract Infection', 'Respiratory Tract Infection'),
        ('Rotavirus', 'Rotavirus'),
        ('Rubella', 'Rubella'),
        ('Sepsis/Infection', 'Sepsis/Infection'),
        ('Septicemia', 'Septicemia'),
        ('Skin', 'Skin'),
        ('Substance', 'Substance'),
        ('Sudden Infant Death', 'Sudden Infant Death'),
        ('Suicide', 'Suicide'),
        ('Tetanus', 'Tetanus'),
        ('Transportation  Accident', 'Transportation  Accident'),
        ('Tuberculosis', 'Tuberculosis'),
        ('Typhoid', 'Typhoid'),
        ('Typhus', 'Typhus'),
        ('Violence', 'Violence'),
        ('West Nile Virus', 'West Nile Virus'),
        ('Yellow Fever', 'Yellow Fever'),
    ], readonly=True)

    _sql_constraints = [
        ('global_id', 'unique(global_id)',
         'The lifecycle already exists in database.')
    ]

    @api.model
    def create(self, vals):
        lifecycle = self.search([
            ('global_id', '=', vals['global_id'])
        ])
        if lifecycle:
            lifecycle.write(vals)
        else:
            lifecycle = super(ChildLifecycleEvent, self).create(vals)
            # Process lifecycle event
            if 'Exit' in lifecycle.type:
                lifecycle.child_id.depart()
            elif lifecycle.type == 'Reinstatement':
                lifecycle.child_id.reinstatement()
        return lifecycle

    @api.model
    def process_commkit(self, commkit_data):
        lifecycle_mapping = mapping.new_onramp_mapping(
            self._name,
            self.env,
            'new_child_lifecyle')
        lifecycle_ids = list()

        for single_data in commkit_data.get('BeneficiaryLifecycleEventList',
                                            [commkit_data]):
            vals = lifecycle_mapping.get_vals_from_connect(single_data)
            lifecycle = self.create(vals)
            lifecycle_ids.append(lifecycle.id)

        return lifecycle_ids
