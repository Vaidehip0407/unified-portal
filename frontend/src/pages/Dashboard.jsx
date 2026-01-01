import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import api from '../api/axios';
import { 
  Zap, Flame, Droplets, Building, ArrowRight, FileText, Upload, 
  ExternalLink, CheckCircle, Clock, User, Shield, AlertCircle,
  MapPin, Phone, Mail, Calendar, Bot
} from 'lucide-react';

const Dashboard = () => {
  const { user } = useAuth();
  const [stats, setStats] = useState({
    documents: 0,
    applications: 0,
    pending: 0,
    completed: 0
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      const [docsRes, appsRes] = await Promise.all([
        api.get('/users/documents'),
        api.get('/applications/')
      ]);
      
      const applications = appsRes.data || [];
      const pending = applications.filter(a => ['pending', 'draft', 'processing'].includes(a.status)).length;
      const completed = applications.filter(a => a.status === 'completed').length;
      
      setStats({
        documents: docsRes.data?.length || 0,
        applications: applications.length,
        pending: pending,
        completed: completed
      });
    } catch (error) {
      console.error('Failed to fetch stats');
    } finally {
      setLoading(false);
    }
  };

  const services = [
    {
      id: 'electricity',
      name: 'Electricity',
      nameGuj: 'વીજળી',
      icon: Zap,
      gradient: 'from-amber-400 to-orange-500',
      iconBg: 'bg-amber-500',
      link: '/electricity',
      color: 'amber'
    },
    {
      id: 'gas',
      name: 'Gas',
      nameGuj: 'ગેસ',
      icon: Flame,
      gradient: 'from-red-400 to-rose-600',
      iconBg: 'bg-red-500',
      link: '/gas',
      color: 'red'
    },
    {
      id: 'water',
      name: 'Water',
      nameGuj: 'પાણી',
      icon: Droplets,
      gradient: 'from-cyan-400 to-blue-500',
      iconBg: 'bg-cyan-500',
      link: '/water',
      color: 'cyan'
    },
    {
      id: 'property',
      name: 'Property',
      nameGuj: 'મિલકત',
      icon: Building,
      gradient: 'from-emerald-400 to-green-600',
      iconBg: 'bg-emerald-500',
      link: '/property',
      color: 'emerald'
    }
  ];

  const statsData = [
    { label: 'Documents', value: stats.documents, icon: FileText, gradient: 'from-emerald-500 to-green-600' },
    { label: 'Applications', value: stats.applications, icon: CheckCircle, gradient: 'from-blue-500 to-indigo-600' },
    { label: 'Pending', value: stats.pending, icon: Clock, gradient: 'from-amber-500 to-orange-600' },
    { label: 'Completed', value: stats.completed, icon: AlertCircle, gradient: 'from-emerald-500 to-teal-600' }
  ];

  return (
    <div className="space-y-6">
      
      {/* Welcome Banner */}
      <div className="relative overflow-hidden rounded-2xl bg-gradient-to-r from-blue-600 via-blue-700 to-blue-800 p-8 text-white shadow-xl">
        <div className="absolute top-0 right-0 w-96 h-96 bg-white/5 rounded-full -mr-48 -mt-48"></div>
        <div className="absolute bottom-0 left-0 w-72 h-72 bg-white/5 rounded-full -ml-36 -mb-36"></div>
        
        <div className="relative z-10">
          <div className="flex items-start gap-4">
            <div className="bg-white/20 backdrop-blur-sm p-4 rounded-2xl">
              <User className="w-10 h-10" />
            </div>
            <div className="flex-1">
              <p className="text-blue-200 text-sm font-medium mb-1">Welcome back</p>
              <h1 className="text-3xl font-bold mb-2">{user?.full_name || 'Citizen'}</h1>
              <p className="text-blue-100">Gujarat State Unified Services Portal</p>
            </div>
          </div>
          
          {/* Quick Info */}
          <div className="flex flex-wrap gap-4 mt-6 pt-6 border-t border-white/20">
            {user?.city && (
              <div className="flex items-center gap-2 text-blue-100">
                <MapPin className="w-4 h-4" />
                <span className="text-sm">{user.city}, Gujarat</span>
              </div>
            )}
            {user?.mobile && (
              <div className="flex items-center gap-2 text-blue-100">
                <Phone className="w-4 h-4" />
                <span className="text-sm">{user.mobile}</span>
              </div>
            )}
            {user?.email && (
              <div className="flex items-center gap-2 text-blue-100">
                <Mail className="w-4 h-4" />
                <span className="text-sm">{user.email}</span>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {statsData.map((stat) => (
          <div 
            key={stat.label} 
            className="bg-white rounded-xl p-4 shadow-lg border border-gray-100 hover:shadow-xl transition-all"
          >
            <div className="flex items-center justify-between">
              <div>
                <p className="text-2xl font-bold text-gray-800">
                  {loading ? '...' : stat.value}
                </p>
                <p className="text-xs text-gray-500 mt-1">{stat.label}</p>
              </div>
              <div className={`bg-gradient-to-br ${stat.gradient} p-3 rounded-lg text-white`}>
                <stat.icon className="w-5 h-5" />
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Quick Actions */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <Link
          to="/documents"
          className="group bg-white p-6 rounded-xl shadow-lg border border-gray-100 hover:shadow-xl transition-all"
        >
          <div className="flex items-center gap-4">
            <div className="bg-gradient-to-br from-emerald-500 to-green-600 p-4 rounded-lg text-white">
              <Upload className="w-6 h-6" />
            </div>
            <div className="flex-1">
              <h3 className="font-bold text-gray-800">Upload Documents</h3>
              <p className="text-sm text-gray-500">Aadhaar, PAN, Bills</p>
            </div>
            <ArrowRight className="w-5 h-5 text-gray-300 group-hover:text-emerald-500 transition-colors" />
          </div>
        </Link>

        <Link
          to="/applications"
          className="group bg-white p-6 rounded-xl shadow-lg border border-gray-100 hover:shadow-xl transition-all"
        >
          <div className="flex items-center gap-4">
            <div className="bg-gradient-to-br from-blue-500 to-indigo-600 p-4 rounded-lg text-white">
              <FileText className="w-6 h-6" />
            </div>
            <div className="flex-1">
              <h3 className="font-bold text-gray-800">My Applications</h3>
              <p className="text-sm text-gray-500">
                {stats.pending > 0 ? `${stats.pending} pending` : 'Track submissions'}
              </p>
            </div>
            <ArrowRight className="w-5 h-5 text-gray-300 group-hover:text-blue-500 transition-colors" />
          </div>
        </Link>
      </div>

      {/* Services Grid */}
      <div>
        <h2 className="text-2xl font-bold text-gray-800 mb-4">Available Services</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {services.map((service) => {
            const Icon = service.icon;
            return (
              <Link
                key={service.id}
                to={service.link}
                className="group bg-white rounded-xl shadow-lg border border-gray-100 overflow-hidden hover:shadow-xl transition-all"
              >
                <div className={`bg-gradient-to-r ${service.gradient} p-6`}>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-4">
                      <div className="bg-white/25 backdrop-blur-sm p-3 rounded-lg">
                        <Icon className="w-7 h-7 text-white" />
                      </div>
                      <div>
                        <h3 className="text-xl font-bold text-white">{service.name}</h3>
                        <p className="text-white/80 text-sm">{service.nameGuj}</p>
                      </div>
                    </div>
                    <ArrowRight className="w-6 h-6 text-white/60 group-hover:translate-x-2 transition-transform" />
                  </div>
                </div>
              </Link>
            );
          })}
        </div>
      </div>

      {/* RPA Demo Section */}
      <Link
        to="/rpa-demo"
        className="group bg-gradient-to-r from-purple-600 to-indigo-600 rounded-xl shadow-lg p-6 text-white hover:shadow-xl transition-all"
      >
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4">
            <div className="bg-white/20 backdrop-blur-sm p-4 rounded-lg">
              <Bot className="w-8 h-8" />
            </div>
            <div>
              <h3 className="text-xl font-bold">Official Government Portals</h3>
              <p className="text-purple-200 text-sm">Direct access to all service providers</p>
            </div>
          </div>
          <ArrowRight className="w-6 h-6 group-hover:translate-x-2 transition-transform" />
        </div>
      </Link>

      {/* Help Section */}
      <div className="bg-gradient-to-r from-emerald-600 to-emerald-700 rounded-xl p-6 text-white">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-lg font-bold">Need Assistance?</h3>
            <p className="text-emerald-200 text-sm mt-1">Contact our support team</p>
          </div>
          <button className="px-6 py-3 bg-white text-emerald-600 rounded-lg font-semibold hover:bg-emerald-50 transition-colors">
            Get Support
          </button>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
