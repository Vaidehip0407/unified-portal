#!/usr/bin/env python3
"""
Update all Gujarat suppliers with official portal URLs and correct information
Based on comprehensive supplier data provided
"""
import json
import os

# Complete supplier data based on the spreadsheet
COMPLETE_SUPPLIERS_DATA = {
    "gas": [
        {
            "id": "gujarat-gas",
            "name": "Gujarat Gas Ltd",
            "type": "government",
            "portal_url": "https://www.gujaratgas.com",
            "name_change_url": "https://iconnect.gujaratgas.com/Portal/outer-service-request_template.aspx",
            "address_change_url": "https://iconnect.gujaratgas.com/Portal/outer-service-request_template.aspx",
            "offline_form_url": "https://iconnect.gujaratgas.com/Portal/Upload.ashx?EncQuery=RbfX54x4vIZzhOBRSRfWTZbXAG7f3AbEg0f7VkvFfGVZliNT3OTix7df9NjIu7AFUPL8Mhq17Uk8uDKp9EzcvQ%3D%3D",
            "api_available": False,
            "online_available": True,
            "rpa_enabled": True,
            "login_required": False,
            "direct_access": True,
            "automation_type": "direct_form",
            "form_type": "web_form",
            "name_change_facility": "Yes (via application form / customer service)",
            "address_change_facility": "Yes (manual update via customer care)"
        },
        {
            "id": "gspc",
            "name": "GSPC Ltd",
            "type": "government",
            "portal_url": "https://www.gspcgroup.com",
            "name_change_url": None,
            "address_change_url": None,
            "offline_form_url": None,
            "api_available": False,
            "online_available": False,
            "rpa_enabled": False,
            "login_required": False,
            "direct_access": False,
            "automation_type": "manual_only",
            "form_type": "office_visit",
            "name_change_facility": "Limited/Not separately available — merging into Gujarat Gas",
            "address_change_facility": "Limited/Manual via customer support",
            "note": "Retail phased out, contact GSPC office"
        },
        {
            "id": "sabarmati-gas",
            "name": "Sabarmati Gas",
            "type": "government",
            "portal_url": "https://www.sabarmatigas.in",
            "name_change_url": None,
            "address_change_url": None,
            "offline_form_url": "https://www.sabarmatigas.in/",
            "api_available": False,
            "online_available": False,
            "rpa_enabled": False,
            "login_required": False,
            "direct_access": False,
            "automation_type": "manual_only",
            "form_type": "office_visit",
            "name_change_facility": "Manual/Offline (contact centre)",
            "address_change_facility": "Manual/Offline",
            "note": "Visit local Sabarmati office"
        },
        {
            "id": "adani-gas",
            "name": "Adani Total Gas Ltd",
            "type": "private",
            "portal_url": "https://www.adanigas.com",
            "name_change_url": "https://www.adanigas.com/name-transfer",
            "address_change_url": "https://www.adanigas.com",
            "offline_form_url": "https://www.adanigas.com",
            "api_available": False,
            "online_available": True,
            "rpa_enabled": True,
            "login_required": True,
            "direct_access": False,
            "automation_type": "login_assisted",
            "form_type": "customer_portal",
            "name_change_facility": "Yes (online name transfer available)",
            "address_change_facility": "Yes (customer self-service on portal)"
        },
        {
            "id": "torrent-gas",
            "name": "Torrent Gas",
            "type": "private",
            "portal_url": "https://connect.torrentgas.com",
            "name_change_url": "https://www.torrentgas.com",
            "address_change_url": "https://connect.torrentgas.com",
            "offline_form_url": "https://connect.torrentgas.com/attachments/static_content/download_page/Name_Transfer_Application_form_all_Locations_domestic.pdf",
            "api_available": False,
            "online_available": True,
            "rpa_enabled": True,
            "login_required": False,
            "direct_access": True,
            "automation_type": "direct_form",
            "form_type": "web_form",
            "name_change_facility": "Yes (application form available)",
            "address_change_facility": "Yes (via customer service)"
        },
        {
            "id": "vadodara-gas",
            "name": "Vadodara Gas Ltd",
            "type": "private",
            "portal_url": "https://www.vgl.co.in",
            "name_change_url": None,
            "address_change_url": None,
            "offline_form_url": "https://www.vgl.co.in/sdm_downloads/affidavit-for-family-member-2-2/",
            "api_available": False,
            "online_available": False,
            "rpa_enabled": False,
            "login_required": False,
            "direct_access": False,
            "automation_type": "manual_only",
            "form_type": "office_visit",
            "name_change_facility": "Yes (name transfer processed manually via office)",
            "address_change_facility": "Yes (via office/agent)"
        },
        {
            "id": "irm-energy",
            "name": "IRM Energy Ltd",
            "type": "private",
            "portal_url": "https://www.irmenergy.com",
            "name_change_url": None,
            "address_change_url": None,
            "offline_form_url": "https://www.irmenergy.com/",
            "api_available": False,
            "online_available": False,
            "rpa_enabled": False,
            "login_required": False,
            "direct_access": False,
            "automation_type": "manual_only",
            "form_type": "customer_service",
            "name_change_facility": "Likely Yes (customer service)",
            "address_change_facility": "Likely Yes (customer service)"
        }
    ],
    "electricity": [
        {
            "id": "pgvcl",
            "name": "Paschim Gujarat Vij Company Ltd (PGVCL)",
            "type": "government",
            "portal_url": "https://www.pgvcl.com",
            "name_change_url": "https://portal.guvnl.in/login.php",
            "address_change_url": "https://portal.guvnl.in/login.php",
            "offline_form_url": "PGVCL office",
            "api_available": False,
            "online_available": True,
            "rpa_enabled": True,
            "login_required": True,
            "direct_access": False,
            "automation_type": "login_assisted",
            "form_type": "guvnl_portal",
            "name_change_facility": "Yes (online request + document verification)",
            "address_change_facility": "Yes (online request, field verification required)"
        },
        {
            "id": "ugvcl",
            "name": "Uttar Gujarat Vij Company Ltd (UGVCL)",
            "type": "government",
            "portal_url": "https://www.ugvcl.com",
            "name_change_url": "https://portal.guvnl.in/login.php",
            "address_change_url": "https://portal.guvnl.in/login.php",
            "offline_form_url": "UGVCL office",
            "api_available": False,
            "online_available": True,
            "rpa_enabled": True,
            "login_required": True,
            "direct_access": False,
            "automation_type": "login_assisted",
            "form_type": "guvnl_portal",
            "name_change_facility": "Yes (application via portal)",
            "address_change_facility": "Yes (mostly offline verification)"
        },
        {
            "id": "mgvcl",
            "name": "Madhya Gujarat Vij Company Ltd (MGVCL)",
            "type": "government",
            "portal_url": "https://www.mgvcl.com",
            "name_change_url": "https://portal.guvnl.in/login.php",
            "address_change_url": "https://portal.guvnl.in/login.php",
            "offline_form_url": "MGVCL office",
            "api_available": False,
            "online_available": True,
            "rpa_enabled": True,
            "login_required": True,
            "direct_access": False,
            "automation_type": "login_assisted",
            "form_type": "guvnl_portal",
            "name_change_facility": "Yes (online initiation, manual approval)",
            "address_change_facility": "Yes (online + site visit)"
        },
        {
            "id": "dgvcl",
            "name": "Dakshin Gujarat Vij Company Ltd (DGVCL)",
            "type": "government",
            "portal_url": "https://www.dgvcl.com",
            "name_change_url": "https://portal.guvnl.in/login.php",
            "address_change_url": "https://portal.guvnl.in/login.php",
            "offline_form_url": "DGVCL office",
            "api_available": False,
            "online_available": True,
            "rpa_enabled": True,
            "login_required": True,
            "direct_access": False,
            "automation_type": "login_assisted",
            "form_type": "guvnl_portal",
            "name_change_facility": "Yes (consumer service request)",
            "address_change_facility": "Yes (address correction supported)"
        },
        {
            "id": "torrent-power",
            "name": "Torrent Power (Ahmedabad/Surat)",
            "type": "private",
            "portal_url": "https://www.torrentpower.com",
            "name_change_url": "https://connect.torrentpower.com",
            "address_change_url": "https://connect.torrentpower.com",
            "offline_form_url": "https://www.torrentpower.com/public/pdf/investors/AHDAHDNameChangeLTENGForm2407191_20211129182958.pdf",
            "api_available": False,
            "online_available": True,
            "rpa_enabled": True,
            "login_required": True,
            "direct_access": False,
            "automation_type": "login_assisted",
            "form_type": "customer_portal",
            "name_change_facility": "Yes (online self-service / assisted)",
            "address_change_facility": "Yes (online request)"
        }
    ],
    "water": [
        {
            "id": "gwssb",
            "name": "Gujarat Water Supply (GWSSB)",
            "type": "government",
            "portal_url": "https://gwssb.gujarat.gov.in",
            "name_change_url": None,
            "address_change_url": None,
            "offline_form_url": "https://watersupply.gujarat.gov.in/forms",
            "api_available": False,
            "online_available": False,
            "rpa_enabled": False,
            "login_required": False,
            "direct_access": False,
            "automation_type": "manual_only",
            "form_type": "office_visit",
            "name_change_facility": "Yes (application based, mostly offline)",
            "address_change_facility": "Yes (manual verification required)"
        },
        {
            "id": "amc-water",
            "name": "AMC (Ahmedabad Municipal Corporation)",
            "type": "government",
            "portal_url": "https://ahmedabadcity.gov.in",
            "name_change_url": None,
            "address_change_url": None,
            "offline_form_url": "AMC office",
            "api_available": False,
            "online_available": True,
            "rpa_enabled": False,
            "login_required": True,
            "direct_access": False,
            "automation_type": "login_assisted",
            "form_type": "municipal_portal",
            "name_change_facility": "Yes (online request + document submission)",
            "address_change_facility": "Yes (online request, ward-level verification)"
        },
        {
            "id": "smc-water",
            "name": "SMC (Surat Municipal Corporation)",
            "type": "government",
            "portal_url": "https://www.suratmunicipal.gov.in",
            "name_change_url": None,
            "address_change_url": None,
            "offline_form_url": "SMC office",
            "api_available": False,
            "online_available": True,
            "rpa_enabled": False,
            "login_required": True,
            "direct_access": False,
            "automation_type": "login_assisted",
            "form_type": "municipal_portal",
            "name_change_facility": "Yes (online initiation, manual approval)",
            "address_change_facility": "Yes (mostly offline verification)"
        },
        {
            "id": "vmc-water",
            "name": "Vadodara Municipal Corporation (VMC)",
            "type": "government",
            "portal_url": "https://vmc.gov.in",
            "name_change_url": None,
            "address_change_url": None,
            "offline_form_url": "VMC office",
            "api_available": False,
            "online_available": False,
            "rpa_enabled": False,
            "login_required": False,
            "direct_access": False,
            "automation_type": "manual_only",
            "form_type": "office_visit",
            "name_change_facility": "Yes (application based)",
            "address_change_facility": "Yes (application based)"
        },
        {
            "id": "rmc-water",
            "name": "Rajkot Municipal Corporation (RMC)",
            "type": "government",
            "portal_url": "https://www.rmc.gov.in",
            "name_change_url": None,
            "address_change_url": None,
            "offline_form_url": "RMC office",
            "api_available": False,
            "online_available": False,
            "rpa_enabled": False,
            "login_required": False,
            "direct_access": False,
            "automation_type": "manual_only",
            "form_type": "office_visit",
            "name_change_facility": "Yes (offline / assisted)",
            "address_change_facility": "Yes (offline / assisted)"
        }
    ],
    "property": [
        {
            "id": "anyror",
            "name": "AnyROR (Revenue Department)",
            "type": "government",
            "portal_url": "https://anyror.gujarat.gov.in",
            "name_change_url": "https://anyror.gujarat.gov.in",
            "address_change_url": "https://anyror.gujarat.gov.in",
            "offline_form_url": "https://revenuedepartment.gujarat.gov.in/e-dhara-forms",
            "api_available": False,
            "online_available": True,
            "rpa_enabled": True,
            "login_required": False,
            "direct_access": True,
            "automation_type": "direct_form",
            "form_type": "web_form",
            "name_change_facility": "Yes (online application, manual mutation approval required)",
            "address_change_facility": "Limited (record correction only)"
        },
        {
            "id": "enagar",
            "name": "e-Nagar Portal",
            "type": "government",
            "portal_url": "https://enagar.gujarat.gov.in",
            "name_change_url": "https://enagar.gujarat.gov.in",
            "address_change_url": "https://enagar.gujarat.gov.in",
            "offline_form_url": "https://revenuedepartment.gujarat.gov.in/e-dhara-forms",
            "api_available": False,
            "online_available": True,
            "rpa_enabled": True,
            "login_required": True,
            "direct_access": False,
            "automation_type": "login_assisted",
            "form_type": "government_portal",
            "name_change_facility": "Yes (property tax mutation request)",
            "address_change_facility": "Yes (address correction via ULB)"
        },
        {
            "id": "municipal-property",
            "name": "Municipal Corporations (AMC, RMC, VMC, SMC & other ULBs)",
            "type": "government",
            "portal_url": "https://urban.gujarat.gov.in",
            "name_change_url": "https://ahmedabadcity.gov.in",
            "address_change_url": "https://ahmedabadcity.gov.in",
            "offline_form_url": "https://revenuedepartment.gujarat.gov.in/e-dhara-forms",
            "api_available": False,
            "online_available": True,
            "rpa_enabled": False,
            "login_required": True,
            "direct_access": False,
            "automation_type": "login_assisted",
            "form_type": "municipal_portal",
            "name_change_facility": "Yes (online initiation, ward-level verification)",
            "address_change_facility": "Yes (online request + physical verification)"
        },
        {
            "id": "edhara-centers",
            "name": "e-Dhara Centers",
            "type": "government",
            "portal_url": "https://landrecords.gujarat.gov.in",
            "name_change_url": "https://edhara.gujarat.gov.in",
            "address_change_url": "https://edhara.gujarat.gov.in",
            "offline_form_url": "https://revenuedepartment.gujarat.gov.in/e-dhara-forms",
            "api_available": False,
            "online_available": True,
            "rpa_enabled": False,
            "login_required": False,
            "direct_access": True,
            "automation_type": "assisted_service",
            "form_type": "service_center",
            "name_change_facility": "Yes (assisted service, document submission)",
            "address_change_facility": "Yes (assisted correction)"
        }
    ]
}

def update_services_data():
    """Update the services_data.json file with complete supplier information"""
    try:
        # Read existing file
        services_file = "backend/app/data/services_data.json"
        
        if os.path.exists(services_file):
            with open(services_file, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
        else:
            existing_data = {}
        
        # Update with complete data
        updated_data = COMPLETE_SUPPLIERS_DATA
        
        # Write updated data
        with open(services_file, 'w', encoding='utf-8') as f:
            json.dump(updated_data, f, indent=2, ensure_ascii=False)
        
        print("✅ Services data updated successfully!")
        print(f"📊 Updated suppliers:")
        for category, suppliers in updated_data.items():
            print(f"   {category.upper()}: {len(suppliers)} suppliers")
        
        return True
        
    except Exception as e:
        print(f"❌ Error updating services data: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Updating all Gujarat suppliers with official portal URLs...")
    success = update_services_data()
    
    if success:
        print("\n🎉 All suppliers updated with correct portal URLs!")
        print("📋 Next steps:")
        print("1. Commit and push changes to GitHub")
        print("2. Deploy to EC2")
        print("3. Test portal redirections")
        print("4. Update frontend to show correct URLs")
    else:
        print("\n❌ Update failed. Please check the error and try again.")