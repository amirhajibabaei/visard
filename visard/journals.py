from visard.rc_settings import cm_to_inches, pt_to_inches


nature = {
    'columns': 2,
    'single': cm_to_inches(8.9),
    'double': cm_to_inches(18.3),
    'single-double': None,
    'page': cm_to_inches(24.7),
}


physical_review = {
    'columns': 2,
    'single': cm_to_inches(8.6),
    'double': cm_to_inches(17.8),
    'single-double': None,
    'page': None,
}
physical_review_letters = physical_review_e = physical_review_x = physical_review


science_advances = {
    'columns': 2,
    'single': 3.5,
    'double': 7.3,
    'single-double': 5.,
    'page': None,
}


article = {
    'columns': 1,
    'single': pt_to_inches(210.),
    'double': pt_to_inches(430.),
    'single-double': pt_to_inches(320.),
    'page': None,
}