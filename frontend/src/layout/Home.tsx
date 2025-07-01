import { Link } from "react-router-dom";

const Home = () => {
    return (
        <div className="min-h-screen bg-green-50">
            {/* Header */}
            <header className="bg-white shadow-sm">
                <div className="container mx-auto px-6 py-4 flex justify-between items-center">
                    <div className="flex items-center">
                        <span className="text-2xl font-bold text-[#405D72]">ERPApp</span>
                    </div>
                    <nav>
                        <ul className="flex space-x-8">
                            <li><a href="#" className="text-[#2b475c] hover:text-[#758694]">Inicio</a></li>
                            <li><a href="#" className="text-gray-600 hover:text-[#758694]">Funciones</a></li>
                            <li><a href="#" className="text-gray-600 hover:text-[#758694]">Nosotros</a></li>
                            <li><a href="#" className="text-gray-600 hover:text-[#758694]">Contacto</a></li>
                        </ul>
                    </nav>
                    <button className="bg-[#405D72] hover:bg-[#2b475c] text-white px-6 py-2 rounded-lg">
                        <Link to={'/login'}>
                            Iniciar Sesión
                        </Link>
                    </button>
                </div>
            </header>

            {/* Hero Section */}
            <section className="bg-[#405D72] text-white py-20">
                <div className="container mx-auto px-6 text-center">
                    <h1 className="text-5xl font-bold mb-6">Optimiza tu empresa con nuestro ERP</h1>
                    <p className="text-xl mb-8 max-w-2xl mx-auto">
                        Automatiza procesos, mejora la productividad y toma decisiones inteligentes con nuestras herramientas de gestión empresarial.
                    </p>
                    <div className="space-x-4">
                        <button className="bg-white text-[#405D72] px-8 py-3 rounded-full font-semibold hover:bg-green-50">
                            Comenzar ahora
                        </button>
                        <button className="border-2 border-white px-8 py-3 rounded-full font-semibold hover:bg-[#2b475c]">
                            Saber más
                        </button>
                    </div>
                </div>
            </section>

            {/* Features Section */}
            <section className="py-20">
                <div className="container mx-auto px-6">
                    <h2 className="text-3xl font-bold text-center text-gray-800 mb-16">Nuestras Soluciones ERP</h2>

                    <div className="grid md:grid-cols-3 gap-10">
                        {[
                            {
                                icon: '✅',
                                title: 'Gestión de Inventario',
                                description: 'Controla tus productos, existencias y almacenes en tiempo real'
                            },
                            {
                                icon: '📦',
                                title: 'Compras y Proveedores',
                                description: 'Gestiona tus órdenes de compra, proveedores y abastecimiento fácilmente'
                            },
                            {
                                icon: '📊',
                                title: 'Reportes Inteligentes',
                                description: 'Visualiza indicadores clave para tomar decisiones estratégicas'
                            }
                        ].map((feature, index) => (
                            <div key={index} className="bg-white p-8 rounded-xl shadow-md text-center hover:shadow-lg transition-shadow">
                                <span className="text-4xl mb-4 inline-block">{feature.icon}</span>
                                <h3 className="text-xl font-semibold text-[#405D72] mb-3">{feature.title}</h3>
                                <p className="text-gray-600">{feature.description}</p>
                            </div>
                        ))}
                    </div>
                </div>
            </section>

            {/* Footer */}
            <footer className="bg-[#112330] text-white py-12">
                <div className="container mx-auto px-6">
                    <div className="flex flex-col md:flex-row justify-between">
                        <div className="mb-8 md:mb-0">
                            <span className="text-2xl font-bold">ERPApp</span>
                            <p className="mt-2 max-w-xs">El ERP que se adapta a tu forma de trabajar</p>
                        </div>
                        <div className="grid grid-cols-2 md:grid-cols-3 gap-8">
                            <div>
                                <h4 className="font-semibold mb-4">Enlaces</h4>
                                <ul className="space-y-2">
                                    <li><a href="#" className="hover:text-[#314e63]">Inicio</a></li>
                                    <li><a href="#" className="hover:text-[#314e63]">Nosotros</a></li>
                                    <li><a href="#" className="hover:text-[#314e63]">Contacto</a></li>
                                </ul>
                            </div>
                            <div>
                                <h4 className="font-semibold mb-4">Legal</h4>
                                <ul className="space-y-2">
                                    <li><a href="#" className="hover:text-[#314e63]">Privacidad</a></li>
                                    <li><a href="#" className="hover:text-[#314e63]">Términos</a></li>
                                </ul>
                            </div>
                            <div>
                                <h4 className="font-semibold mb-4">Social</h4>
                                <ul className="space-y-2">
                                    <li><a href="#" className="hover:text-[#314e63]">Twitter</a></li>
                                    <li><a href="#" className="hover:text-[#314e63]">Instagram</a></li>
                                    <li><a href="#" className="hover:text-[#314e63]">Facebook</a></li>
                                </ul>
                            </div>
                        </div>
                    </div>
                    <div className="border-t border-[#2b475c] mt-12 pt-8 text-center text-[#314e63]">
                        <p>© {new Date().getFullYear()} ERPApp. Todos los derechos reservados.</p>
                    </div>
                </div>
            </footer>
        </div>
    );
};

export default Home;