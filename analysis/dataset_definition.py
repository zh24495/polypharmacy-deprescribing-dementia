from ehrql import create_dataset, codelist_from_csv
from ehrql.tables.tpp import patients, practice_registrations, clinical_events, addresses

dataset = create_dataset()

index_date = "2015-01-01"

dementia_codelist = codelist_from_csv(
    "codelists/bristol-any-dementia-snomed-ct-v14.csv",
    column="code",
)

##Derive Variables
dataset.sex = patients.sex
dataset.age = patients.age_on(index_date)
dataset.date_of_death = patients.date_of_death
dataset.first_dementia_code = (
    clinical_events.where(clinical_events.snomedct_code.is_in(dementia_codelist))
    .sort_by(clinical_events.date)
    .first_for_patient()
    .snomedct_code)
dataset.imd = addresses.for_patient_on(index_date).imd_rounded

##Apply criteria
aged_over_64 = dataset.age > 64
has_registration = practice_registrations.for_patient_on(
    index_date
).exists_for_patient()

has_dementia = (
    clinical_events.where(clinical_events.snomedct_code.is_in(dementia_codelist))
    .sort_by(clinical_events.date)
    .first_for_patient()
    ).exists_for_patient()

is_alive = patients.is_alive_on(index_date)

known_sex = patients.sex != "unknown"
known_imd = dataset.imd>0


known_imd = dataset.imd>0
dataset.define_population(has_registration & has_dementia & aged_over_64 & is_alive & known_sex & known_imd)
