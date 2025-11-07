export type Language = "en" | "fr" | "ar"

export interface Translations {
  // Header
  searchPlaceholder: string
  categories: string
  deals: string
  buildGuide: string
  language: string
  compare: string
  menu: string

  // Homepage
  heroTitle: string
  heroSubtitle: string
  heroDescription: string
  searchPlaceholder2: string
  searchParts: string
  popular: string
  compareTopRetailers: string
  shopByCategory: string
  categoryDescription: string
  buildYourPc: string
  comingSoon: string
  buildDescription: string
  compatibilityChecking: string
  budgetOptimization: string
  performanceBenchmarks: string
  getNotified: string
  heroSubtitlePart1: string
  heroSubtitlePart2: string

  // Categories
  processors: string
  graphicsCards: string
  memory: string
  storage: string
  motherboards: string
  powerSupply: string
  monitors: string
  peripherals: string
  products: string

  // Search Results
  searchResults: string
  showingResults: string
  resultsFound: string
  filters: string
  activeFilters: string
  clearAll: string
  priceRange: string
  brand: string
  availability: string
  inStock: string
  limitedStock: string
  outOfStock: string
  preOrder: string
  sortBy: string
  relevance: string
  priceLowToHigh: string
  priceHighToLow: string
  customerRating: string
  newestFirst: string
  mostPopular: string
  gridView: string
  listView: string
  compareAction: string
  viewStores: string
  viewDetails: string
  stores: string
  reviews: string
  resultsFoundLabel: string
  mobileFilters: string

  // Product Detail
  backToSearch: string
  startingFrom: string
  availableAt: string
  compareAllStores: string
  keyFeatures: string
  priceComparison: string
  compareFromStores: string
  bestPrice: string
  visitStore: string
  specifications: string
  relatedProducts: string
  updated: string
  freeShipping: string
  shipping: string
  pricesUpdated: string
  verifyPrice: string

  // Footer
  footerDescription: string
  support: string
  helpCenter: string
  contactUs: string
  privacyPolicy: string
  termsOfService: string
  contact: string
  morocco: string
  footerCopyright: string

  // Common
  mad: string
  to: string
  bestSeller: string
}

export const translations: Record<Language, Translations> = {
  en: {
    // Header
    searchPlaceholder: "Search for PC parts...",
    categories: "Categories",
    deals: "Deals",
    buildGuide: "Build Guide",
    language: "Language",
    compare: "Compare",
    menu: "Menu",

    // Homepage
    heroTitle: "Find the Best PC Parts",
    heroSubtitle:
      "Compare prices, availability, find the best deals on CPUs, GPUs RAM, and more from trusted Moroccan retailers.",
    heroDescription:
      "Compare prices, availability, find find the best deals on CPUs, GPUs RAM, and more from trusted Moroccan retailers.",
    searchPlaceholder2: "Search for graphics cards, processors, RAM...",
    searchParts: "Search Parts",
    popular: "Popular:",
    compareTopRetailers: "Compare prices across top Moroccan retailers",
    shopByCategory: "Shop by Category",
    categoryDescription: "Browse our extensive collection of PC components and peripherals",
    buildYourPc: "Build Your Own PC",
    comingSoon: "Coming Soon",
    buildDescription:
      "Get personalized PC build recommendations based on your budget and needs. Our intelligent system will suggest compatible components and find the best prices.",
    compatibilityChecking: "Compatibility checking",
    budgetOptimization: "Budget optimization",
    performanceBenchmarks: "Performance benchmarks",
    getNotified: "Get Notified",
    heroSubtitlePart1: "Prices in",
    heroSubtitlePart2: "Morocco",

    // Categories
    processors: "Processors",
    graphicsCards: "Graphics Cards",
    memory: "Memory (RAM)",
    storage: "Storage",
    motherboards: "Motherboards",
    powerSupply: "Power Supply",
    monitors: "Monitors",
    peripherals: "Peripherals",
    products: "Products",

    // Search Results
    searchResults: "Search Results",
    showingResults: "Showing results for",
    resultsFound: "results found",
    filters: "Filters",
    activeFilters: "Active Filters",
    clearAll: "Clear All",
    priceRange: "Price Range",
    brand: "Brand",
    availability: "Availability",
    inStock: "In Stock",
    limitedStock: "Limited Stock",
    outOfStock: "Out of Stock",
    preOrder: "Pre-order",
    sortBy: "Sort by",
    relevance: "Relevance",
    priceLowToHigh: "Price: Low to High",
    priceHighToLow: "Price: High to Low",
    customerRating: "Customer Rating",
    newestFirst: "Newest First",
    mostPopular: "Most Popular",
    gridView: "Grid view",
    listView: "List view",
    compareAction: "Compare",
    viewStores: "View Stores",
    viewDetails: "View Details",
    stores: "stores",
    reviews: "reviews",
    resultsFoundLabel: "results found",
    mobileFilters: "Filters",

    // Product Detail
    backToSearch: "Back to search results",
    startingFrom: "Starting from",
    availableAt: "Available at",
    compareAllStores: "Compare All Stores",
    keyFeatures: "Key Features",
    priceComparison: "Price Comparison",
    compareFromStores: "Compare prices from",
    bestPrice: "Best Price",
    visitStore: "Visit Store",
    specifications: "Specifications",
    relatedProducts: "Related Products",
    updated: "Updated",
    freeShipping: "Free shipping",
    shipping: "shipping",
    pricesUpdated: "Prices are updated regularly and may vary. Please verify final price on retailer website.",
    verifyPrice: "Verify Price",

    // Footer
    footerDescription:
      "Morocco's leading PC parts price comparison platform. Find the best deals from trusted retailers.",
    support: "Support",
    helpCenter: "Help Center",
    contactUs: "Contact Us",
    privacyPolicy: "Privacy Policy",
    termsOfService: "Terms of Service",
    contact: "Contact",
    morocco: "Morocco",
    footerCopyright: "All rights reserved. Prices in MAD (Moroccan Dirham).",

    // Common
    mad: "MAD",
    to: "to",
    bestSeller: "Best Seller",
  },

  fr: {
    // Header
    searchPlaceholder: "Rechercher des composants PC...",
    categories: "Catégories",
    deals: "Offres",
    buildGuide: "Guide de Montage",
    language: "Langue",
    compare: "Comparer",
    menu: "Menu",

    // Homepage
    heroTitle: "Trouvez les Meilleurs Prix de Composants PC",
    heroSubtitle:
      "Comparez les prix, vérifiez la disponibilité et trouvez les meilleures offres sur les CPU, GPU, RAM et plus encore chez les détaillants marocains de confiance.",
    heroDescription:
      "Comparez les prix, vérifiez la disponibilité et trouvez les meilleures offres sur les CPU, GPU, RAM et plus encore chez les détaillants marocains de confiance.",
    searchPlaceholder2: "Rechercher des cartes graphiques, des processeurs, de la RAM...",
    searchParts: "Rechercher",
    popular: "Populaire:",
    compareTopRetailers: "Comparez les prix chez les meilleurs détaillants marocains",
    shopByCategory: "Acheter par Catégorie",
    categoryDescription: "Parcourez notre vaste collection de composants PC et périphériques",
    buildYourPc: "Construisez Votre PC",
    comingSoon: "Bientôt Disponible",
    buildDescription:
      "Obtenez des recommandations personnalisées de configuration PC basées sur votre budget et vos besoins. Notre système intelligent suggérera des composants compatibles et trouvera les meilleurs prix.",
    compatibilityChecking: "Vérification de compatibilité",
    budgetOptimization: "Optimisation du budget",
    performanceBenchmarks: "Tests de performance",
    getNotified: "Être Notifié",
    heroSubtitlePart1: "au",
    heroSubtitlePart2: "Maroc",

    // Categories
    processors: "Processeurs CPU",
    graphicsCards: "Cartes Graphiques GPU",
    memory: "Mémoire (RAM)",
    storage: "Stockage SSD/HDD",
    motherboards: "Cartes Mères",
    powerSupply: "Alimentation PSU",
    monitors: "Moniteurs",
    peripherals: "Périphériques",
    products: "Produits",

    // Search Results
    searchResults: "Résultats de Recherche",
    showingResults: "Affichage des résultats pour",
    resultsFound: "résultats trouvés",
    filters: "Filtres",
    activeFilters: "Filtres Actifs",
    clearAll: "Tout Effacer",
    priceRange: "Gamme de Prix",
    brand: "Marque",
    availability: "Disponibilité",
    inStock: "En Stock",
    limitedStock: "Stock Limité",
    outOfStock: "Rupture de Stock",
    preOrder: "Pré-commande",
    sortBy: "Trier par",
    relevance: "Pertinence",
    priceLowToHigh: "Prix: Croissant",
    priceHighToLow: "Prix: Décroissant",
    customerRating: "Note Client",
    newestFirst: "Plus Récent",
    mostPopular: "Plus Populaire",
    gridView: "Vue grille",
    listView: "Vue liste",
    compareAction: "Comparer",
    viewStores: "Voir Magasins",
    viewDetails: "Voir Détails",
    stores: "magasins",
    reviews: "avis",
    resultsFoundLabel: "résultats trouvés",
    mobileFilters: "Filtres",

    // Product Detail
    backToSearch: "Retour aux résultats",
    startingFrom: "À partir de",
    availableAt: "Disponible chez",
    compareAllStores: "Comparer Tous les Magasins",
    keyFeatures: "Caractéristiques Clés",
    priceComparison: "Comparaison de Prix",
    compareFromStores: "Comparer les prix de",
    bestPrice: "Meilleur Prix",
    visitStore: "Visiter le Magasin",
    specifications: "Spécifications",
    relatedProducts: "Produits Similaires",
    updated: "Mis à jour",
    freeShipping: "Livraison gratuite",
    shipping: "livraison",
    pricesUpdated:
      "Les prix sont mis à jour régulièrement et peuvent varier. Veuillez vérifier le prix final sur le site du détaillant.",
    verifyPrice: "Vérifier le Prix",

    // Footer
    footerDescription:
      "Plateforme leader de comparaison de prix de composants PC au Maroc. Trouvez les meilleures offres chez des revendeurs de confiance.",
    support: "Support",
    helpCenter: "Centre d'Aide",
    contactUs: "Nous Contacter",
    privacyPolicy: "Politique de Confidentialité",
    termsOfService: "Conditions d'Utilisation",
    contact: "Contact",
    morocco: "Maroc",
    footerCopyright: "Tous droits réservés. Prices in MAD (Dirham Marocain).",

    // Common
    mad: "MAD",
    to: "à",
    bestSeller: "Meilleure Vente",
  },

  ar: {
    // Header
    searchPlaceholder: "البحث عن قطع الكمبيوتر...",
    categories: "الفئات",
    deals: "العروض",
    buildGuide: "دليل التجميع",
    language: "اللغة",
    compare: "مقارنة",
    menu: "القائمة",

    // Homepage
    heroTitle: "اعثر على أفضل أسعار قطع الكمبيوتر",
    heroSubtitle:
      "قارن الأسعار، تحقق من التوفر، واعثر على أفضل العروض على المعالجات وكروت الرسوميات والذاكرة والمزيد من تجار التجزئة المغاربة الموثوقين.",
    heroDescription:
      "قارن الأسعار، تحقق من التوفر، واعثر على أفضل العروض على المعالجات وكروت الرسوميات والذاكرة والمزيد من تجار التجزئة المغاربة الموثوقين.",
    searchPlaceholder2: "البحث عن كروت رسوميات، معالجات، ذاكرة RAM...",
    searchParts: "البحث",
    popular: "شائع:",
    compareTopRetailers: "قارن الأسعار عند أفضل تجار التجزئة المغاربة",
    shopByCategory: "تسوق حسب الفئة",
    categoryDescription: "تصفح مجموعتنا الواسعة من مكونات الكمبيوتر والملحقات",
    buildYourPc: "اجمع حاسوبك الخاص",
    comingSoon: "قريباً",
    buildDescription:
      "احصل على توصيات مخصصة لتجميع الكمبيوتر بناءً على ميزانيتك واحتياجاتك. سيقترح نظامنا الذكي مكونات متوافقة ويجد أفضل الأسعار.",
    compatibilityChecking: "فحص التوافق",
    budgetOptimization: "تحسين الميزانية",
    performanceBenchmarks: "اختبارات الأداء",
    getNotified: "احصل على إشعار",
    heroSubtitlePart1: "في",
    heroSubtitlePart2: "المغرب",

    // Categories
    processors: "المعالجات CPU",
    graphicsCards: "كروت الرسوميات GPU",
    memory: "الذاكرة RAM",
    storage: "التخزين SSD/HDD",
    motherboards: "اللوحات الأم",
    powerSupply: "مزود الطاقة PSU",
    monitors: "الشاشات",
    peripherals: "الملحقات",
    products: "منتجات",

    // Search Results
    searchResults: "نتائج البحث",
    showingResults: "عرض النتائج لـ",
    resultsFound: "نتيجة موجودة",
    filters: "المرشحات",
    activeFilters: "المرشحات النشطة",
    clearAll: "مسح الكل",
    priceRange: "نطاق السعر",
    brand: "العلامة التجارية",
    availability: "التوفر",
    inStock: "متوفر",
    limitedStock: "مخزون محدود",
    outOfStock: "غير متوفر",
    preOrder: "طلب مسبق",
    sortBy: "ترتيب حسب",
    relevance: "الصلة",
    priceLowToHigh: "السعر: من الأقل للأعلى",
    priceHighToLow: "السعر: من الأعلى للأقل",
    customerRating: "تقييم العملاء",
    newestFirst: "الأحدث أولاً",
    mostPopular: "الأكثر شعبية",
    gridView: "عرض الشبكة",
    listView: "عرض القائمة",
    compareAction: "مقارنة",
    viewStores: "عرض المتاجر",
    viewDetails: "عرض التفاصيل",
    stores: "متاجر",
    reviews: "مراجعات",
    resultsFoundLabel: "نتيجة موجودة",
    mobileFilters: "المرشحات",

    // Product Detail
    backToSearch: "العودة لنتائج البحث",
    startingFrom: "يبدأ من",
    availableAt: "متوفر في",
    compareAllStores: "مقارنة جميع المتاجر",
    keyFeatures: "الميزات الرئيسية",
    priceComparison: "مقارنة الأسعار",
    compareFromStores: "مقارنة الأسعار من",
    bestPrice: "أفضل سعر",
    visitStore: "زيارة المتجر",
    specifications: "المواصفات",
    relatedProducts: "منتجات ذات صلة",
    updated: "محدث",
    freeShipping: "شحن مجاني",
    shipping: "شحن",
    pricesUpdated: "يتم تحديث الأسعار بانتظام وقد تختلف. يرجى التحقق من السعر النهائي على موقع بائع التجزئة.",
    verifyPrice: "تحقق من السعر",

    // Footer
    footerDescription:
      "منصة المغرب الرائدة لمقارنة أسعار قطع الكمبيوتر. اعثر على أفضل العروض من تجار التجزئة الموثوقين.",
    support: "الدعم",
    helpCenter: "مركز المساعدة",
    contactUs: "اتصل بنا",
    privacyPolicy: "سياسة الخصوصية",
    termsOfService: "شروط الخدمة",
    contact: "اتصال",
    morocco: "المغرب",
    footerCopyright: "جميع الحقوق محفوظة. الأسعار بالدرهم المغربي (MAD).",

    // Common
    mad: "درهم",
    to: "إلى",
    bestSeller: "الأكثر مبيعاً",
  },
}

export const getTranslation = (language: Language): Translations => {
  return translations[language] || translations.en
}

export const formatPrice = (price: number, language: Language): string => {
  const t = getTranslation(language)
  return `${price.toLocaleString()} ${t.mad}`
}
