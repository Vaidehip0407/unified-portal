import React, { useState, useEffect } from 'react';
import { ExternalLink, Info, CheckCircle, AlertCircle, Clock } from 'lucide-react';

const PortalRedirect = ({ supplierId, serviceType = 'name_change' }) => {
  const [supplierData, setSupplierData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchSupplierData();
  }, [supplierId]);

  const fetchSupplierData = async () => {
    try {
      const response = await fetch('/api/services/data');
      const data = await response.json();
      
      // Find supplier in all categories
      let supplier = null;
      for (const category of Object.values(data)) {
        supplier = category.find(s => s.id === supplierId);
        if (supplier) break;
      }
      
      setSupplierData(supplier);
    } catch (error) {
      console.error('Error fetching supplier data:', error);
    } finally {
      setLoading(false);
    }
  };

  const getServiceUrl = () => {
    if (!supplierData) return null;
    
    switch (serviceType) {
      case 'name_change':
        return supplierData.name_change_url;
      case 'address_change':
        return supplierData.address_change_url;
      default:
        return supplierData.portal_url;
    }
  };

  const getAutomationStatus = () => {
    if (!supplierData) return null;
    
    const { automation_type, online_available, rpa_enabled } = supplierData;
    
    if (automation_type === 'direct_form' && rpa_enabled) {
      return {
        type: 'automated',
        icon: CheckCircle,
        color: 'text-green-600',
        bgColor: 'bg-green-50',
        borderColor: 'border-green-200',
        message: 'Automated form filling available'
      };
    } else if (automation_type === 'login_assisted') {
      return {
        type: 'assisted',
        icon: Clock,
        color: 'text-yellow-600',
        bgColor: 'bg-yellow-50',
        borderColor: 'border-yellow-200',
        message: 'Login assistance available'
      };
    } else if (online_available) {
      return {
        type: 'manual',
        icon: Info,
        color: 'text-blue-600',
        bgColor: 'bg-blue-50',
        borderColor: 'border-blue-200',
        message: 'Manual form filling required'
      };
    } else {
      return {
        type: 'offline',
        icon: AlertCircle,
        color: 'text-red-600',
        bgColor: 'bg-red-50',
        borderColor: 'border-red-200',
        message: 'Office visit required'
      };
    }
  };

  if (loading) {
    return (
      <div className="animate-pulse">
        <div className="h-32 bg-gray-200 rounded-lg"></div>
      </div>
    );
  }

  if (!supplierData) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-4">
        <div className="flex items-center">
          <AlertCircle className="h-5 w-5 text-red-600 mr-2" />
          <span className="text-red-800">Supplier information not found</span>
        </div>
      </div>
    );
  }

  const serviceUrl = getServiceUrl();
  const automationStatus = getAutomationStatus();
  const StatusIcon = automationStatus?.icon;

  return (
    <div className="bg-white border border-gray-200 rounded-lg shadow-sm">
      {/* Header */}
      <div className="px-6 py-4 border-b border-gray-200">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-lg font-semibold text-gray-900">
              {supplierData.name}
            </h3>
            <p className="text-sm text-gray-600 capitalize">
              {supplierData.type} • {serviceType.replace('_', ' ')}
            </p>
          </div>
          {StatusIcon && (
            <div className={`flex items-center px-3 py-1 rounded-full ${automationStatus.bgColor} ${automationStatus.borderColor} border`}>
              <StatusIcon className={`h-4 w-4 ${automationStatus.color} mr-1`} />
              <span className={`text-xs font-medium ${automationStatus.color}`}>
                {automationStatus.type.toUpperCase()}
              </span>
            </div>
          )}
        </div>
      </div>

      {/* Content */}
      <div className="px-6 py-4">
        {/* Automation Status */}
        {automationStatus && (
          <div className={`mb-4 p-3 rounded-lg ${automationStatus.bgColor} ${automationStatus.borderColor} border`}>
            <div className="flex items-center">
              <StatusIcon className={`h-5 w-5 ${automationStatus.color} mr-2`} />
              <span className={`text-sm font-medium ${automationStatus.color}`}>
                {automationStatus.message}
              </span>
            </div>
          </div>
        )}

        {/* Service Information */}
        <div className="space-y-3">
          <div>
            <label className="text-sm font-medium text-gray-700">
              {serviceType === 'name_change' ? 'Name Change Facility' : 'Address Change Facility'}:
            </label>
            <p className="text-sm text-gray-600 mt-1">
              {serviceType === 'name_change' 
                ? supplierData.name_change_facility 
                : supplierData.address_change_facility}
            </p>
          </div>

          {/* Portal Links */}
          <div className="space-y-2">
            {serviceUrl && (
              <div>
                <label className="text-sm font-medium text-gray-700">Official Portal:</label>
                <a
                  href={serviceUrl}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-center text-blue-600 hover:text-blue-800 text-sm mt-1 group"
                >
                  <ExternalLink className="h-4 w-4 mr-1" />
                  <span className="group-hover:underline">
                    {serviceUrl.replace('https://', '').replace('http://', '')}
                  </span>
                </a>
              </div>
            )}

            {supplierData.offline_form_url && (
              <div>
                <label className="text-sm font-medium text-gray-700">Download Form:</label>
                <a
                  href={supplierData.offline_form_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-center text-green-600 hover:text-green-800 text-sm mt-1 group"
                >
                  <ExternalLink className="h-4 w-4 mr-1" />
                  <span className="group-hover:underline">Download PDF Form</span>
                </a>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Action Buttons */}
      <div className="px-6 py-4 bg-gray-50 border-t border-gray-200 rounded-b-lg">
        <div className="flex space-x-3">
          {serviceUrl && (
            <a
              href={serviceUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="flex-1 bg-blue-600 text-white text-center py-2 px-4 rounded-md hover:bg-blue-700 transition-colors flex items-center justify-center"
            >
              <ExternalLink className="h-4 w-4 mr-2" />
              Visit Official Portal
            </a>
          )}
          
          {supplierData.automation_type === 'direct_form' && supplierData.rpa_enabled && (
            <button
              onClick={() => {
                // Trigger automation
                window.dispatchEvent(new CustomEvent('startAutomation', {
                  detail: { supplierId, serviceType }
                }));
              }}
              className="flex-1 bg-green-600 text-white text-center py-2 px-4 rounded-md hover:bg-green-700 transition-colors flex items-center justify-center"
            >
              <CheckCircle className="h-4 w-4 mr-2" />
              Start Automation
            </button>
          )}
        </div>
      </div>
    </div>
  );
};

export default PortalRedirect;