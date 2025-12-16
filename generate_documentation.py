#!/usr/bin/env python3
"""
Generate comprehensive PDF documentation for the Motorcycle Repair Shops project
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Image
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from datetime import datetime
import os

def create_documentation_pdf():
    """Generate comprehensive PDF documentation"""

    filename = "Motorcycle_Repair_Shops_Project_Documentation.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter,
                           rightMargin=72, leftMargin=72,
                           topMargin=72, bottomMargin=18)

    # Container for the 'Flowable' objects
    elements = []

    # Define styles
    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1e40af'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )

    heading1_style = ParagraphStyle(
        'CustomHeading1',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#2563eb'),
        spaceAfter=12,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )

    heading2_style = ParagraphStyle(
        'CustomHeading2',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#3b82f6'),
        spaceAfter=10,
        spaceBefore=10,
        fontName='Helvetica-Bold'
    )

    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontSize=11,
        spaceAfter=12,
        alignment=TA_JUSTIFY,
        leading=14
    )

    code_style = ParagraphStyle(
        'Code',
        parent=styles['Code'],
        fontSize=9,
        fontName='Courier',
        textColor=colors.HexColor('#1f2937'),
        backColor=colors.HexColor('#f3f4f6'),
        leftIndent=20,
        rightIndent=20,
        spaceAfter=12,
        spaceBefore=12
    )

    # Title Page
    elements.append(Spacer(1, 2*inch))
    elements.append(Paragraph("🏍️", title_style))
    elements.append(Paragraph("Motorcycle Repair Shops", title_style))
    elements.append(Paragraph("European Directory", title_style))
    elements.append(Spacer(1, 0.5*inch))
    elements.append(Paragraph("Project Documentation", heading1_style))
    elements.append(Spacer(1, 0.3*inch))
    elements.append(Paragraph(f"Generated: {datetime.now().strftime('%B %d, %Y')}", body_style))
    elements.append(PageBreak())

    # Table of Contents
    elements.append(Paragraph("Table of Contents", heading1_style))
    elements.append(Spacer(1, 0.2*inch))

    toc_data = [
        ["1.", "Project Overview"],
        ["2.", "Technology Stack"],
        ["3.", "Development Timeline"],
        ["4.", "Key Features"],
        ["5.", "Architecture & Components"],
        ["6.", "Data Management"],
        ["7.", "Setup & Installation"],
        ["8.", "Project Structure"],
        ["9.", "Future Enhancements"],
    ]

    toc_table = Table(toc_data, colWidths=[0.5*inch, 5*inch])
    toc_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#1f2937')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    elements.append(toc_table)
    elements.append(PageBreak())

    # 1. Project Overview
    elements.append(Paragraph("1. Project Overview", heading1_style))
    elements.append(Spacer(1, 0.2*inch))

    overview_text = """
    The Motorcycle Repair Shops European Directory is a modern, completely FREE web application
    designed to help motorcycle enthusiasts and riders find reliable repair shops across 27 European
    countries. Built with cutting-edge web technologies, this application provides an intuitive
    interface for discovering, searching, and locating motorcycle service centers throughout Europe.
    """
    elements.append(Paragraph(overview_text, body_style))
    elements.append(Spacer(1, 0.2*inch))

    # Key Highlights
    elements.append(Paragraph("Key Highlights:", heading2_style))

    highlights = [
        ["✓", "Covers 27 European Union countries"],
        ["✓", "3000+ motorcycle repair shops"],
        ["✓", "100% FREE - No API costs, no billing required"],
        ["✓", "Interactive maps powered by OpenStreetMap"],
        ["✓", "Fully responsive design for all devices"],
        ["✓", "Real-time search and filtering capabilities"],
        ["✓", "Modern, gradient-based UI design"],
    ]

    highlights_table = Table(highlights, colWidths=[0.5*inch, 5.5*inch])
    highlights_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#059669')),
        ('TEXTCOLOR', (1, 0), (1, -1), colors.HexColor('#1f2937')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    elements.append(highlights_table)
    elements.append(Spacer(1, 0.3*inch))

    # 2. Technology Stack
    elements.append(Paragraph("2. Technology Stack", heading1_style))
    elements.append(Spacer(1, 0.2*inch))

    elements.append(Paragraph("Frontend Technologies:", heading2_style))
    frontend_text = """
    <b>Next.js 16:</b> The latest version of React's premier framework, providing server-side
    rendering, static site generation, and optimized performance out of the box.<br/><br/>

    <b>React 19:</b> The newest version of React, offering improved performance, enhanced hooks,
    and better developer experience with concurrent features.<br/><br/>

    <b>TypeScript:</b> Provides type safety throughout the application, reducing bugs and
    improving code maintainability.<br/><br/>

    <b>Tailwind CSS 4:</b> Utility-first CSS framework enabling rapid UI development with
    consistent design patterns and responsive layouts.
    """
    elements.append(Paragraph(frontend_text, body_style))
    elements.append(Spacer(1, 0.2*inch))

    elements.append(Paragraph("Mapping Solution:", heading2_style))
    mapping_text = """
    <b>Leaflet + OpenStreetMap:</b> A completely FREE mapping solution that requires no API keys,
    no billing setup, and has no usage limits. Leaflet is a lightweight JavaScript library for
    interactive maps, while OpenStreetMap provides community-driven, open-source map data.
    """
    elements.append(Paragraph(mapping_text, body_style))
    elements.append(Spacer(1, 0.2*inch))

    elements.append(Paragraph("Data Management:", heading2_style))
    data_text = """
    <b>CSV File Storage:</b> Shop data is stored in CSV format for easy management and portability.
    The application includes a custom CSV parser that handles quoted fields and complex data structures.<br/><br/>

    <b>Supabase (Optional):</b> PostgreSQL-based backend service for advanced features and
    real-time capabilities. The free tier is sufficient for most use cases.
    """
    elements.append(Paragraph(data_text, body_style))
    elements.append(PageBreak())

    # 3. Development Timeline
    elements.append(Paragraph("3. Development Timeline", heading1_style))
    elements.append(Spacer(1, 0.2*inch))

    timeline_text = """
    The project was developed through several iterative phases, each adding significant
    functionality and improvements:
    """
    elements.append(Paragraph(timeline_text, body_style))
    elements.append(Spacer(1, 0.2*inch))

    timeline_data = [
        ["Phase", "Development Focus", "Key Achievements"],
        ["Phase 1\nWeek 1",
         "Initial Setup",
         "• Created Next.js project\n• Basic project structure\n• Initial commit"],
        ["Phase 2\nWeek 2-3",
         "Core Features",
         "• Country filtering system\n• Google Maps integration (later replaced)\n• Modern UI with gradients\n• Responsive design implementation"],
        ["Phase 3\nWeek 4",
         "Configuration & Docs",
         "• Comprehensive setup guides\n• API key configuration\n• Setup checker script\n• Quick start documentation"],
        ["Phase 4\nWeek 5",
         "Maps Migration",
         "• Replaced Google Maps with OpenStreetMap\n• Integrated Leaflet library\n• Removed API key requirements\n• Made app 100% FREE to use"],
        ["Phase 5\nWeek 6-7",
         "Data Enhancement",
         "• Added CSV file support\n• Built custom CSV parser\n• Migrated to CSV data storage\n• Data setup documentation"],
        ["Phase 6\nRecent",
         "Optimization",
         "• Fixed shop list display issues\n• Optimized for 3000+ shops\n• Performance improvements\n• Bug fixes and refinements"],
    ]

    timeline_table = Table(timeline_data, colWidths=[1.2*inch, 2.2*inch, 2.6*inch])
    timeline_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2563eb')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#d1d5db')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    elements.append(timeline_table)
    elements.append(PageBreak())

    # 4. Key Features
    elements.append(Paragraph("4. Key Features", heading1_style))
    elements.append(Spacer(1, 0.2*inch))

    # Feature 1: Interactive Maps
    elements.append(Paragraph("4.1 Interactive Maps", heading2_style))
    maps_text = """
    The application features a fully interactive map powered by Leaflet and OpenStreetMap. Users can:
    <br/><br/>
    • View all motorcycle shops as custom-styled markers on the map<br/>
    • Zoom and pan to explore different regions<br/>
    • Click on markers to see detailed shop information in popups<br/>
    • Automatic map centering based on filtered results<br/>
    • Smart bounds adjustment when filtering by country<br/>
    • Custom motorcycle-themed markers with gradient styling
    <br/><br/>
    The map automatically adjusts its view based on the selected shops, ensuring users always
    see the most relevant information without manual navigation.
    """
    elements.append(Paragraph(maps_text, body_style))
    elements.append(Spacer(1, 0.2*inch))

    # Feature 2: Country Filtering
    elements.append(Paragraph("4.2 Country Filtering System", heading2_style))
    country_text = """
    A sophisticated country filtering system allows users to narrow down their search:
    <br/><br/>
    • Desktop view displays an elegant grid of all 27 EU countries<br/>
    • Mobile view uses a dropdown selector for space efficiency<br/>
    • Each country displays its flag emoji and name<br/>
    • Real-time shop count updates when countries are selected<br/>
    • "All Countries" option to reset the filter<br/>
    • Smooth animations and hover effects for better UX
    <br/><br/>
    The system covers: Austria, Belgium, Bulgaria, Croatia, Cyprus, Czech Republic, Denmark,
    Estonia, Finland, France, Germany, Greece, Hungary, Ireland, Italy, Latvia, Lithuania,
    Luxembourg, Malta, Netherlands, Poland, Portugal, Romania, Slovakia, Slovenia, Spain, and Sweden.
    """
    elements.append(Paragraph(country_text, body_style))
    elements.append(Spacer(1, 0.2*inch))

    # Feature 3: Smart Search
    elements.append(Paragraph("4.3 Smart Search Functionality", heading2_style))
    search_text = """
    The application includes a powerful search system that enables users to quickly find specific shops:
    <br/><br/>
    • Search by shop name, city, street address, or country code<br/>
    • Real-time filtering as users type<br/>
    • Case-insensitive search for better usability<br/>
    • Search results counter showing matching shops<br/>
    • Works in combination with country filtering<br/>
    • Optimized for performance even with 3000+ shops
    <br/><br/>
    The search functionality uses React's useMemo hook to optimize performance, ensuring smooth
    filtering even with large datasets.
    """
    elements.append(Paragraph(search_text, body_style))
    elements.append(Spacer(1, 0.2*inch))

    # Feature 4: Dual View Modes
    elements.append(Paragraph("4.4 Dual View Modes", heading2_style))
    views_text = """
    Users can switch between two distinct viewing modes:
    <br/><br/>
    <b>Map View:</b> Displays all shops on an interactive map with custom markers. Perfect for
    geographical exploration and finding shops in specific areas.
    <br/><br/>
    <b>List View:</b> Shows shops in a beautiful card-based grid layout. Each card includes:
    <br/>
    • Shop name with gradient header<br/>
    • Complete address information<br/>
    • Contact details (phone, email, website)<br/>
    • Country flag and name<br/>
    • Direct link to Google Maps<br/>
    • Hover effects and smooth transitions
    <br/><br/>
    The toggle between views is seamless, maintaining the current filter and search state.
    """
    elements.append(Paragraph(views_text, body_style))
    elements.append(PageBreak())

    # Feature 5: Responsive Design
    elements.append(Paragraph("4.5 Responsive Design", heading2_style))
    responsive_text = """
    The application is fully responsive and optimized for all device sizes:
    <br/><br/>
    <b>Desktop (1920px+):</b> Full-featured interface with grid-based country selector,
    large map view, and 3-column shop cards.
    <br/><br/>
    <b>Laptop (1024px - 1919px):</b> Optimized layout with 2-column shop cards and
    adjusted spacing for comfortable viewing.
    <br/><br/>
    <b>Tablet (768px - 1023px):</b> Adaptive layout with 2-column cards, touch-optimized
    controls, and appropriate font sizes.
    <br/><br/>
    <b>Mobile (320px - 767px):</b> Single-column layout, dropdown country selector,
    stacked controls, and touch-friendly interface elements.
    <br/><br/>
    All interactions are optimized for touch and mouse input, ensuring a great experience
    regardless of device type.
    """
    elements.append(Paragraph(responsive_text, body_style))
    elements.append(PageBreak())

    # 5. Architecture & Components
    elements.append(Paragraph("5. Architecture & Components", heading1_style))
    elements.append(Spacer(1, 0.2*inch))

    arch_text = """
    The application follows a modern React architecture with clear separation of concerns:
    """
    elements.append(Paragraph(arch_text, body_style))
    elements.append(Spacer(1, 0.2*inch))

    # Component descriptions
    elements.append(Paragraph("5.1 MotorcycleShops Component", heading2_style))
    comp1_text = """
    The main component that orchestrates the entire application:
    <br/><br/>
    • Manages application state (shops, filters, search, view mode)<br/>
    • Fetches data from CSV file on component mount<br/>
    • Implements useMemo for optimized filtering<br/>
    • Renders header with statistics<br/>
    • Coordinates child components<br/>
    • Handles view mode switching
    <br/><br/>
    This component serves as the container for all other components and manages the data flow
    throughout the application.
    """
    elements.append(Paragraph(comp1_text, body_style))
    elements.append(Spacer(1, 0.2*inch))

    elements.append(Paragraph("5.2 CountrySelector Component", heading2_style))
    comp2_text = """
    A smart component that provides country filtering functionality:
    <br/><br/>
    • Displays all 27 EU countries with flags<br/>
    • Responsive grid layout (desktop) / dropdown (mobile)<br/>
    • Highlights selected country<br/>
    • Passes selection back to parent component<br/>
    • Smooth animations and hover effects
    <br/><br/>
    The component automatically adapts its layout based on screen size, providing the best
    user experience for each device type.
    """
    elements.append(Paragraph(comp2_text, body_style))
    elements.append(Spacer(1, 0.2*inch))

    elements.append(Paragraph("5.3 ShopMap Component", heading2_style))
    comp3_text = """
    An advanced mapping component built with React-Leaflet:
    <br/><br/>
    • Dynamically imported to prevent SSR issues<br/>
    • Custom map markers with motorcycle icons<br/>
    • Automatic bounds adjustment based on shops<br/>
    • Interactive popups with shop information<br/>
    • Links to external mapping services<br/>
    • Optimized rendering for large datasets
    <br/><br/>
    The component includes a MapBoundsHandler sub-component that automatically adjusts the map
    view when the shop list changes, ensuring users always see relevant data.
    """
    elements.append(Paragraph(comp3_text, body_style))
    elements.append(Spacer(1, 0.2*inch))

    elements.append(Paragraph("5.4 CSV Parser Utility", heading2_style))
    comp4_text = """
    A custom-built CSV parsing utility that handles data loading:
    <br/><br/>
    • Parses CSV files with proper quote handling<br/>
    • Transforms flat CSV data into structured objects<br/>
    • Maps country names to ISO codes<br/>
    • Handles missing or malformed data gracefully<br/>
    • Supports various CSV field formats
    <br/><br/>
    The parser is designed to handle the complexities of real-world CSV data, including quoted
    fields, commas within values, and varying data quality.
    """
    elements.append(Paragraph(comp4_text, body_style))
    elements.append(PageBreak())

    # 6. Data Management
    elements.append(Paragraph("6. Data Management", heading1_style))
    elements.append(Spacer(1, 0.2*inch))

    data_text = """
    The application uses a CSV-based data management system for simplicity and portability:
    """
    elements.append(Paragraph(data_text, body_style))
    elements.append(Spacer(1, 0.2*inch))

    elements.append(Paragraph("Data Source:", heading2_style))
    source_text = """
    All motorcycle shop data is sourced from OpenStreetMap (OSM), the world's largest
    collaborative mapping project. The data includes shops tagged as:
    <br/><br/>
    • shop=motorcycle - Dedicated motorcycle shops<br/>
    • craft=motorcycle - Motorcycle craft and repair services<br/>
    • amenity=car_repair with motorcycle=yes - Multi-service repair shops
    <br/><br/>
    Data is fetched using the Overpass API, which allows querying OSM data with complex filters.
    """
    elements.append(Paragraph(source_text, body_style))
    elements.append(Spacer(1, 0.2*inch))

    elements.append(Paragraph("Data Structure:", heading2_style))
    structure_text = """
    Each shop record contains the following information:
    <br/><br/>
    • Unique ID<br/>
    • Shop name<br/>
    • Geographic coordinates (latitude, longitude)<br/>
    • Complete address (street, house number, postal code, city)<br/>
    • Country code (ISO 3166-1 alpha-2)<br/>
    • Contact information (phone, email, website)<br/>
    • Additional tags from OpenStreetMap
    <br/><br/>
    The data is stored in a CSV file located at /public/data/eu_motorcycle_repairs.csv, making
    it easy to update and maintain.
    """
    elements.append(Paragraph(structure_text, body_style))
    elements.append(Spacer(1, 0.2*inch))

    elements.append(Paragraph("Data Updates:", heading2_style))
    updates_text = """
    The project includes a Python script (scripts/fetch_osm_data.py) that can fetch fresh data
    from OpenStreetMap. This allows the database to be updated with new shops and changes to
    existing entries. The script can be run with:
    <br/><br/>
    <font name="Courier">npm run fetch:data</font>
    <br/><br/>
    This ensures the application always has access to the most current information.
    """
    elements.append(Paragraph(updates_text, body_style))
    elements.append(PageBreak())

    # 7. Setup & Installation
    elements.append(Paragraph("7. Setup & Installation", heading1_style))
    elements.append(Spacer(1, 0.2*inch))

    setup_text = """
    Setting up the project is straightforward and requires minimal configuration:
    """
    elements.append(Paragraph(setup_text, body_style))
    elements.append(Spacer(1, 0.2*inch))

    elements.append(Paragraph("Prerequisites:", heading2_style))
    prereq_text = """
    • Node.js 18 or higher<br/>
    • npm or yarn package manager<br/>
    • Git for version control<br/>
    • (Optional) Supabase account for advanced features
    <br/><br/>
    <b>Important:</b> No API keys are required for maps! The application uses OpenStreetMap,
    which is completely free and requires no registration.
    """
    elements.append(Paragraph(prereq_text, body_style))
    elements.append(Spacer(1, 0.2*inch))

    elements.append(Paragraph("Installation Steps:", heading2_style))

    install_code = """1. Clone the repository:
   git clone &lt;repository-url&gt;
   cd motorcycle

2. Install dependencies:
   npm install

3. (Optional) Set up environment variables:
   cp .env.local.example .env.local
   # Edit .env.local with your Supabase credentials if needed

4. Start the development server:
   npm run dev

5. Open your browser to http://localhost:3000
"""
    elements.append(Paragraph(install_code, code_style))
    elements.append(Spacer(1, 0.2*inch))

    elements.append(Paragraph("Available Scripts:", heading2_style))
    scripts_text = """
    • <font name="Courier">npm run dev</font> - Start development server with hot reload<br/>
    • <font name="Courier">npm run build</font> - Create optimized production build<br/>
    • <font name="Courier">npm start</font> - Start production server<br/>
    • <font name="Courier">npm run fetch:data</font> - Fetch latest data from OpenStreetMap
    """
    elements.append(Paragraph(scripts_text, body_style))
    elements.append(PageBreak())

    # 8. Project Structure
    elements.append(Paragraph("8. Project Structure", heading1_style))
    elements.append(Spacer(1, 0.2*inch))

    structure_code = """motorcycle/
├── src/
│   ├── app/                      # Next.js App Router
│   │   ├── layout.tsx           # Root layout component
│   │   ├── page.tsx             # Home page
│   │   ├── globals.css          # Global styles
│   │   └── favicon.ico          # Site favicon
│   ├── components/
│   │   ├── CountrySelector/     # Country filtering component
│   │   │   └── index.tsx
│   │   ├── MotorcycleShops/     # Main shops component
│   │   │   └── index.tsx
│   │   └── ShopMap/             # Interactive map component
│   │       └── index.tsx
│   ├── data/
│   │   └── countries.ts         # EU countries configuration
│   └── utils/
│       └── csvParser.ts         # CSV parsing utility
├── public/
│   └── data/
│       └── eu_motorcycle_repairs.csv  # Shop data (3000+ entries)
├── scripts/
│   └── fetch_osm_data.py        # OSM data fetching script
├── supabase/
│   └── supabaseClient.js        # Supabase configuration
├── package.json                  # Dependencies and scripts
├── tsconfig.json                 # TypeScript configuration
├── tailwind.config.js            # Tailwind CSS configuration
├── next.config.ts                # Next.js configuration
└── README.md                     # Project documentation
"""
    elements.append(Paragraph(structure_code, code_style))
    elements.append(Spacer(1, 0.2*inch))

    structure_text = """
    The project follows Next.js 13+ App Router conventions with a clear separation between
    presentation components, utilities, and data. This structure makes the codebase easy to
    navigate and maintain.
    """
    elements.append(Paragraph(structure_text, body_style))
    elements.append(PageBreak())

    # 9. Future Enhancements
    elements.append(Paragraph("9. Future Enhancements", heading1_style))
    elements.append(Spacer(1, 0.2*inch))

    future_text = """
    The project has a strong foundation and several potential enhancements could further
    improve its value:
    """
    elements.append(Paragraph(future_text, body_style))
    elements.append(Spacer(1, 0.2*inch))

    enhancements = [
        ["Feature", "Description", "Benefit"],
        ["User Reviews",
         "Allow users to rate and review shops",
         "Community-driven quality insights"],
        ["Advanced Filters",
         "Filter by services, certifications, ratings",
         "More precise shop discovery"],
        ["Route Planning",
         "Integration with routing services",
         "Help plan motorcycle trips"],
        ["Favorites System",
         "Save preferred shops to a personal list",
         "Quick access to trusted shops"],
        ["Mobile App",
         "Native iOS/Android applications",
         "Better mobile experience"],
        ["Offline Support",
         "Progressive Web App features",
         "Access without internet connection"],
        ["Multilingual",
         "Support for multiple European languages",
         "Wider accessibility"],
        ["Business Portal",
         "Allow shops to claim and update listings",
         "More accurate, current information"],
    ]

    enhancements_table = Table(enhancements, colWidths=[1.3*inch, 2.4*inch, 2.3*inch])
    enhancements_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2563eb')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#d1d5db')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    elements.append(enhancements_table)
    elements.append(Spacer(1, 0.3*inch))

    # Conclusion
    elements.append(Paragraph("Conclusion", heading1_style))
    conclusion_text = """
    The Motorcycle Repair Shops European Directory represents a modern approach to solving a
    real-world problem: helping motorcycle riders find reliable service centers across Europe.
    By leveraging cutting-edge web technologies and open-source mapping solutions, the project
    delivers a professional, feature-rich application that is completely free to use and deploy.
    <br/><br/>
    The development journey showcased in this document demonstrates the evolution from initial
    concept through multiple iterations, each adding value and improving the user experience.
    The decision to migrate from Google Maps to OpenStreetMap particularly highlights the
    project's commitment to accessibility and eliminating barriers to entry.
    <br/><br/>
    With 3000+ shops across 27 countries, responsive design, intelligent search and filtering,
    and an intuitive interface, this application provides real value to the European motorcycle
    community while serving as an excellent example of modern web development practices.
    """
    elements.append(Paragraph(conclusion_text, body_style))
    elements.append(Spacer(1, 0.5*inch))

    # Footer
    footer_text = f"""
    <br/><br/>
    ═══════════════════════════════════════════════════════════════════
    <br/><br/>
    <b>Project:</b> Motorcycle Repair Shops - European Directory<br/>
    <b>Documentation Generated:</b> {datetime.now().strftime('%B %d, %Y at %I:%M %p')}<br/>
    <b>Technology:</b> Next.js 16 • React 19 • TypeScript • Tailwind CSS 4<br/>
    <b>Repository:</b> github.com/Svpriyaa2808/motorcycle
    """
    elements.append(Paragraph(footer_text, body_style))

    # Build PDF
    doc.build(elements)
    print(f"✓ PDF documentation generated successfully: {filename}")
    return filename

if __name__ == "__main__":
    create_documentation_pdf()
