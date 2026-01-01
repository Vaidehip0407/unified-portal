// Complete services data for Gujarat
export const servicesData = {
  gas: [
    {
      id: "torrent_gas",
      name: "Torrent Gas",
      type: "private",
      portal: "https://connect.torrentgas.com/",
      online: true,
      rpa: true
    },
    {
      id: "adani_gas",
      name: "Adani Total Gas Ltd",
      type: "private",
      portal: "https://www.adanigas.com/",
      online: true,
      rpa: true
    },
    {
      id: "gujarat_gas",
      name: "Gujarat Gas Ltd",
      type: "government",
      portal: "https://www.gujaratgas.com/",
      online: true,
      rpa: true
    },
    {
      id: "sabarmati_gas",
      name: "Sabarmati Gas",
      type: "government",
      portal: "https://www.sabarmatigas.in/",
      online: false,
      rpa: false
    },
    {
      id: "irm_energy",
      name: "IRM Energy Ltd",
      type: "private",
      portal: "https://www.irmenergy.com/",
      online: false,
      rpa: false
    },
    {
      id: "vadodara_gas",
      name: "Vadodara Gas Ltd",
      type: "private",
      portal: "https://www.vgl.co.in/",
      online: false,
      rpa: false
    }
  ],
  electricity: [
    {
      id: "torrent_power",
      name: "Torrent Power",
      type: "private",
      portal: "https://connect.torrentpower.com/",
      online: true,
      rpa: true
    },
    {
      id: "pgvcl",
      name: "PGVCL",
      type: "government",
      portal: "https://www.pgvcl.com/",
      online: true,
      rpa: true
    },
    {
      id: "ugvcl",
      name: "UGVCL",
      type: "government",
      portal: "https://www.ugvcl.com/",
      online: true,
      rpa: true
    },
    {
      id: "mgvcl",
      name: "MGVCL",
      type: "government",
      portal: "https://www.mgvcl.com/",
      online: true,
      rpa: true
    },
    {
      id: "dgvcl",
      name: "DGVCL",
      type: "government",
      portal: "https://www.dgvcl.com/",
      online: true,
      rpa: true
    }
  ],
  water: [
    {
      id: "amc",
      name: "AMC (Ahmedabad)",
      type: "government",
      portal: "https://ahmedabadcity.gov.in/",
      online: true,
      rpa: true
    },
    {
      id: "smc",
      name: "SMC (Surat)",
      type: "government",
      portal: "https://www.suratmunicipal.gov.in/",
      online: true,
      rpa: false
    },
    {
      id: "vmc",
      name: "VMC (Vadodara)",
      type: "government",
      portal: "https://vmc.gov.in/",
      online: true,
      rpa: false
    },
    {
      id: "rmc",
      name: "RMC (Rajkot)",
      type: "government",
      portal: "https://www.rmc.gov.in/",
      online: true,
      rpa: false
    },
    {
      id: "gwssb",
      name: "GWSSB",
      type: "government",
      portal: "https://gwssb.gujarat.gov.in/",
      online: false,
      rpa: false
    }
  ],
  property: [
    {
      id: "anyror",
      name: "AnyROR",
      type: "government",
      portal: "https://anyror.gujarat.gov.in/",
      online: true,
      rpa: true
    },
    {
      id: "enagar",
      name: "e-Nagar",
      type: "government",
      portal: "https://enagar.gujarat.gov.in/",
      online: true,
      rpa: false
    },
    {
      id: "edhara",
      name: "e-Dhara",
      type: "government",
      portal: "https://edhara.gujarat.gov.in/",
      online: true,
      rpa: false
    },
    {
      id: "indiafilings",
      name: "IndiaFilings",
      type: "private",
      portal: "https://www.indiafilings.com/",
      online: true,
      rpa: false
    },
    {
      id: "ezylegal",
      name: "ezyLegal",
      type: "private",
      portal: "https://www.ezylegal.in/",
      online: true,
      rpa: false
    }
  ]
};

export const getServicesByCategory = (category) => {
  return servicesData[category] || [];
};

export const getOnlineServices = (category) => {
  return getServicesByCategory(category).filter(s => s.online);
};

export const getRPAServices = (category) => {
  return getServicesByCategory(category).filter(s => s.rpa);
};

export const getServiceById = (category, id) => {
  return getServicesByCategory(category).find(s => s.id === id);
};

export const getServiceNames = (category) => {
  return getServicesByCategory(category).map(s => s.name);
};
