import sqlite3

def setup_database():
    conn = sqlite3.connect('progress_tracker.db')
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE Users (
            UserID INTEGER PRIMARY KEY,
            Username TEXT,
            PasswordHash TEXT,
            Salt TEXT
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE Subjects (
            SubjectID INTEGER PRIMARY KEY,
            SubjectName TEXT
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE Topics (
            TopicID INTEGER,
            SubjectID INTEGER,
            TopicName TEXT,
            PRIMARY KEY (TopicID, SubjectID),
            FOREIGN KEY (SubjectID) REFERENCES Subjects(SubjectID)
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE User_Subjects (
            UserID INTEGER,
            SubjectID INTEGER,
            PRIMARY KEY (UserID, SubjectID),
            FOREIGN KEY (UserID) REFERENCES Users(UserID),
            FOREIGN KEY (SubjectID) REFERENCES Subjects(SubjectID)

        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE User_Topic_Progress (
            UserID INTEGER,
            TopicID INTEGER,
            SubjectID INTEGER,
            TopicCompleted BOOLEAN,
            ConfidenceLevel INTEGER,
            LastReviewed DATE,
            PRIMARY KEY (UserID, TopicID, SubjectID),
            FOREIGN KEY (UserID) REFERENCES Users(UserID),
            FOREIGN KEY (TopicID) REFERENCES Topics(TopicID)
            FOREIGN KEY (SubjectID) REFERENCES Subjects(SubjectID)
        );

        """
    )

    SUBJECTS = {
        "Mathematics": [
            "Algebraic expressions",
            "Index laws",
            "Expanding brackets",
            "Factorising",
            "Negative and fractional indices",
            "Surds",
            "Rationalising denominators",
            "Quadratics",
            "Solving quadratic equations",
            "Completing the square",
            "Functions",
            "Quadratic graphs",
            "The discriminant",
            "Modelling with quadratics",
            "Equations and inequalities",
            "Linear simultaneous equations",
            "Quadratic simutaneous equations",
            "Simultaneous equations on graphs",
            "Linear inequalities",
            "Quadratic inequalities",
            "Inequalities on graphs",
            "Regions",
            "Graphs and transformations",
            "Cubic grpahs",
            "Quartic graphs",
            "Reciprocal graphs",
            "Points of intersection",
            "Translating graphs",
            "Stretching graphs",
            "Transforming functions",
            "Straight line graphs",
            "y=mx+c",
            "Equations of straight lines",
            "Parallel and perpendicular lines",
            "Length and area",
            "Modelling with straight lines",
            "Circles",
            "Midpoints and perpendicular bisectors",
            "Equation of a circle",
            "Intersections of straight lines and circles",
            "Use tangent and chord properties",
            "Circles and triangles",
            "Algebraic methods",
            "Algebraic fractions",
            "Dividing polynomials",
            "The factor theorem",
            "Mathematical proof",
            "Methods of proof",
            "The binomial expansion",
            "Pascal's triangle",
            "Factorial notation",
            "The binomial expansion",
            "Solving binomial problems",
            "Binomial estimation",
            "Trigonometric ratios",
            "The cosine rule",
            "The sine rule",
            "Areas of triangles",
            "Solving triangle problems",
            "Graphs of sine, cosine and tangent",
            "Transforming trigonometric graphs",
            "Trigonometric identities and equations",
            "Angles in all four quadrants",
            "Exact values of trigonometric ratios",
            "Trigonometric identities",
            "Simple trigonometric equations",
            "Harder trigonometric equations",
            "Equations and identities",
            "Vectors",
            "Vectors",
            "Representing vectors",
            "Magnitude and direction",
            "Position vectors",
            "Solving geometric problems",
            "Modelling with vectors",
            "Differentiation",
            "Gradients of curves",
            "Finding the derivative",
            "Differentiation xn",
            "Differentiation quadratics",
            "Differentiating functions with two or more terms",
            "Gradients , tangents and normal",
            "Increasing and decreasing functions",
            "Second order derivatives",
            "Stationary points",
            "Sketching gradient functions",
            "Modelling with differentiation",
            "Integration",
            "Integrating xn",
            "Indefinite integrals",
            "Finding functions",
            "Definite integrals",
            "Areas under curves",
            "Areas under the x-axis",
            "Areas between curves and lines",
            "Exponentials and loogarithms",
            "Exponential functions",
            "y=ex",
            "Exponential modelling",
            "Logarithms",
            "Laws of logarithms",
            "Solving equations using logarithms",
            "Working with natural logarithms",
            "Logarithms and non-linear data"
        ],

        "Computer Science": [
            "Programming basics",
            "Selection",
            "Iteration",
            "Arrays",
            "Subroutines",
            "Files and exception handling",
            "Solving logic problems",
            "Structured programming",
            "Writing and interpreting algorithms",
            "Testing and evaluation",
            "Abstraction and automation",
            "Finite state machines",
            "Number systems",
            "Bits, bytes and binary",
            "Binary arithmetic and the representation of fractions",
            "Bitmapped graphics",
            "Digital representation of sound",
            "Data compression and encryption algorithms",
            "Hardware and software",
            "Role of an operating system",
            "Programming language classification",
            "Programming language translators",
            "Logic gates",
            "Boolean algebra",
            "Internal computer hardware",
            "The processor",
            "The processor instruction set",
            "Assembly language",
            "Input-output devices",
            "Secondary storage devices",
            "Communication methods",
            "Network topology",
            "Client-server and peer-to-peer",
            "Wireless networking, CSMA and SSID",
            "Communication and privacy",
            "The challenges of the digital age",
            "Queues",
            "Lists",
            "Stacks",
            "Hash tables and dictionaries",
            "Graphs",
            "Trees",
            "Vectors",
            "Recursive algorithms",
            "Big-O notation",
            "Searching and sorting",
            "Graph-traversal algorithms",
            "Optimisation algorithms",
            "Limits of computation",
            "Mealy machines",
            "Sets",
            "Regular expressions",
            "The Turing machine",
            "Backus-Naur Form",
            "Reverse Polish notation",
            "Structure of the Internet",
            "Packet switching and routers",
            "Internet security",
            "TCP/IP, standard application layer protocols",
            "IP addresses",
            "Client server model",
            "Entity relationship modelling",
            "Relational databases and normalisation",
            "Introduction to SQL",
            "Defining and updating tables using SQL",
            "Systematic approah to problem solving",
            "OOP and functional programming",
            "Basic concepts of object-oriented programming",
            "Object-oriented design principles",
            "Functional programming",
            "Function application",
            "Lists in functional programming",
            "Big Data"
        ],

        "Physics": [
            "Matter and radiation",
            "Inside the atom",
            "Stable and unstable nuclei",
            "Photons",
            "Particles and antiparticles",
            "Particle interactions",
            "Quarks and leptons",
            "The particle zoo",
            "Particle sorting",
            "Leptons at work",
            "Quarks and antiquarks",
            "Conservation rules",
            "Quantum phenomena",
            "The photoelectric effect",
            "More about photoelectricity",
            "Collisions of electrons with atoms",
            "Energy levels in atoms",
            "Energy levels and spectra",
            "Wave-particle duality",
            "Waves",
            "Waves and vibrations",
            "Measuring waves",
            "Wave properties 1",
            "Wave properties 2",
            "Stationary and progressive waves",
            "More about stationary waves on strings",
            "Using an oscilloscope",
            "Optics",
            "Refraction of light",
            "More about refraction",
            "Total internal reflection",
            "Double slit interference",
            "More about interference",
            "Diffraction",
            "The diffraction grating",
            "Forces in equilibrium",
            "Vectors and scalars",
            "Balanced forces",
            "The principle of moments",
            "More on moments",
            "Stability",
            "Equilibrium rules",
            "Statics calculations",
            "On the move",
            "Speed and velocity",
            "Acceleration",
            "Motion along a straight line at constant acceleration",
            "Free fall",
            "Motion graphs",
            "More calculations on motion along a straight line",
            "Projectile motion 1",
            "Projectile motion 2",
            "Newton's laws of motion",
            "Force and acceleration",
            "Using F = ma",
            "Terminal speed",
            "On the road",
            "vehicle safety",
            "Forces and momentum",
            "Momentum and impulse",
            "Impact forces",
            "Conservation of momentum",
            "Elastic and inelastic collisions",
            "Explosions",
            "Work, energy and power",
            "Work and energy",
            "Kinetic energy and potential energy",
            "Power",
            "Energy and efficiency",
            "Materials",
            "Density",
            "Springs",
            "Deformation of solids",
            "More about stress and strain",
            "Electric current",
            "Current and charge",
            "Potential difference and power",
            "Resistance",
            "Components and their characteristics",
            "DC circuits",
            "Circuit rules",
            "More about resistance",
            "Electromotive force and internal resistance",
            "More about circuit calculations",
            "The potential divider"
        ]
    }

    subject_id = 1
    for subject, topic_list in SUBJECTS.items():
        cursor.execute(
            """
            INSERT INTO Subjects (SubjectID, SubjectName)
            VALUES (?, ?)
            """,
            (subject_id, subject)
        )

        for topic_id, topic in enumerate(topic_list):
            cursor.execute(
                """
                INSERT INTO Topics (TopicID, SubjectID, TopicName)
                VALUES (?, ?, ?)
                """,
                (topic_id + 1, subject_id, topic)
            )
        
        subject_id += 1
    
    conn.commit()
    conn.close()