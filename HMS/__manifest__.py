{
    "name": "Hospital Management System",
    "summary": "A comprehensive system to manage hospital operations.",
    "description": "This module helps in managing patients, doctors, and departments within a hospital.",
    "author": "Omar Ayman",
    "category": "Healthcare",
    "version": "17.0.0.1.0",
    "depends": ["base", "crm"],
    "application": True,
    "data": [
        "security/group.xml",
        "views/base_manus.xml",
        "views/hms_patient.xml",
        "views/hms_department.xml",
        "views/hms_doctor.xml",
        "security/ir.model.access.csv",
    ]
}
