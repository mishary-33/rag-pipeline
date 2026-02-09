def create_test_cases():
        """Create test cases with ground truth"""
        test_cases = [
        {
            "query": "What is the primary purpose of the RAND Program Classification Tool (R-PCT)?",
            "language": "English",
            "type": "factual",
            "expected_source": "RAND_RR487z1_english.pdf",
            "answerable": True
        },
        {
            "query": "ما هي الأدوات المستخدمة لتقييم الصحة النفسية في التقارير المرفقة؟",
            "language": "Arabic",
            "type": "factual",
            "expected_source": "RAND_RR1562z1.arabic.pdf",
            "answerable": True
        },
        {
            "query": "Explain the three-phase iterative process used to develop the R-PCT.",
            "language": "English",
            "type": "complex",
            "expected_source": "RAND_RR487z1_english.pdf",
            "answerable": True
        },
        {
            "query": "كيف يساهم تقرير RAND في تحسين سياسات الرعاية الصحية في الشرق الأوسط؟",
            "language": "Arabic",
            "type": "complex",
            "expected_source": "RAND_RR1681z1.arabic.pdf",
            "answerable": True
        },
        {
            "query": "What is the specific definition of 'program' used in the R-PCT framework?",
            "language": "English",
            "type": "factual",
            "expected_source": "RAND_RR487z1_english.pdf",
            "answerable": True
        },
        {
            "query": "Does the report mention the use of Python for data analysis?",
            "language": "English",
            "type": "no-info",
            "expected_source": 0,
            "answerable": False
        },
        {
            "query": "ما هي النسبة المئوية للجنود الذين يعانون من اضطراب ما بعد الصدمة حسب دراسة تانيليان وجايكوكس؟",
            "language": "Arabic",
            "type": "factual",
            "expected_source": "RAND_RR487z1_english.pdf",
            "answerable": True
        },
        {
            "query": "How many military personnel were included in the survey regarding TBI symptoms?",
            "language": "English",
            "type": "factual",
            "expected_source": "RAND_RR487z1_english.pdf",
            "answerable": True
        },
        {
            "query": "هل يتضمن التقرير معلومات عن أسعار النفط في عام 2026؟",
            "language": "Arabic",
            "type": "no-info",
            "expected_source": 0,
            "answerable": False
        },
        {
            "query": "Who sponsored the research conducted in the Forces and Resources Policy Center?",
            "language": "English",
            "type": "factual",
            "expected_source": "RAND_RR487z1_english.pdf",
            "answerable": True
        },
        {
            "query": "Describe the taxonomy created for DoD psychological health programs.",
            "language": "English",
            "type": "complex",
            "expected_source": "RAND_RR487z1_english.pdf",
            "answerable": True
        },
        {
            "query": "ما هو دور مركز التميز للدفاع في تحسين الصحة النفسية؟",
            "language": "Arabic",
            "type": "factual",
            "expected_source": "RAND_RR1562z1.arabic.pdf",
            "answerable": True
        },
        {
            "query": "How does the R-PCT distinguish between a 'program' and 'routine services'?",
            "language": "English",
            "type": "complex",
            "expected_source": "RAND_RR487z1_english.pdf",
            "answerable": True
        },
        {
            "query": "Does the document provide a list of symptoms for Traumatic Brain Injury (TBI)?",
            "language": "English",
            "type": "factual",
            "expected_source": "RAND_RR487z1_english.pdf",
            "answerable": True
        },
        {
            "query": "ما هي التوصيات الرئيسية لتعزيز المرونة النفسية لدى العسكريين؟",
            "language": "Arabic",
            "type": "complex",
            "expected_source": "RAND_RR1681z1.arabic.pdf",
            "answerable": True
        },
        {
            "query": "What are the key dimensions of program comparison in the R-PCT?",
            "language": "English",
            "type": "factual",
            "expected_source": "RAND_RR487z1_english.pdf",
            "answerable": True
        },
        {
            "query": "How many programs were evaluated during the reliability testing phase?",
            "language": "English",
            "type": "factual",
            "expected_source": "RAND_RR487z1_english.pdf",
            "answerable": True
        },
        {
            "query": "هل هناك ذكر لتطبيقات الذكاء الاصطناعي في تشخيص الاكتئاب؟",
            "language": "Arabic",
            "type": "no-info",
            "expected_source": 0,
            "answerable": False
        },
        {
            "query": "What is the relationship between deployments and mental health problems in the 2007 report?",
            "language": "English",
            "type": "complex",
            "expected_source": "RAND_RR487z1_english.pdf",
            "answerable": True
        },
        {
            "query": "Explain the concept of 'operational guidance' mentioned in the R-PCT report.",
            "language": "English",
            "type": "complex",
            "expected_source": "RAND_RR487z1_english.pdf",
            "answerable": True
        },
        {
            "query": "ما هي الفئات المستهدفة من أداة تصنيف البرامج؟",
            "language": "Arabic",
            "type": "factual",
            "expected_source": "RAND_RR1562z1.arabic.pdf",
            "answerable": True
        },
        {
            "query": "Identify the primary external stakeholders interested in R-PCT findings.",
            "language": "English",
            "type": "factual",
            "expected_source": "RAND_RR487z1_english.pdf",
            "answerable": True
        },
        {
            "query": "Is there a mention of the 'Innovative Practices' web page in the text?",
            "language": "English",
            "type": "factual",
            "expected_source": "RAND_RR487z1_english.pdf",
            "answerable": True
        },
        {
            "query": "كيف تم التحقق من موثوقية أداة R-PCT؟",
            "language": "Arabic",
            "type": "complex",
            "expected_source": "RAND_RR487z1_english.pdf",
            "answerable": True
        },
        {
            "query": "What is the purpose of the RAND National Defense Research Institute (NDRI)?",
            "language": "English",
            "type": "factual",
            "expected_source": "RAND_RR487z1_english.pdf",
            "answerable": True
        },
        {
            "query": "How does the report address the 'duplication of effort' problem in DoD?",
            "language": "English",
            "type": "complex",
            "expected_source": "RAND_RR487z1_english.pdf",
            "answerable": True
        },
        {
            "query": "ما هي الميزانية المخصصة لبرامج الصحة النفسية المذكورة؟",
            "language": "Arabic",
            "type": "no-info",
            "expected_source": 0,
            "answerable": False
        },
        {
            "query": "What are the common psychological health conditions discussed in the introduction?",
            "language": "English",
            "type": "factual",
            "expected_source": "RAND_RR487z1_english.pdf",
            "answerable": True
        },
        {
            "query": "Explain the importance of peer review in RAND reports.",
            "language": "English",
            "type": "complex",
            "expected_source": "RAND_RR487z1_english.pdf",
            "answerable": True
        },
        {
            "query": "هل يوفر التقرير دليلاً لاستخدام أداة R-PCT؟",
            "language": "Arabic",
            "type": "factual",
            "expected_source": "RAND_RR1562z1.arabic.pdf",
            "answerable": True
        },
        {
            "query": "What are the implications of frequent redeployments according to the text?",
            "language": "English",
            "type": "complex",
            "expected_source": "RAND_RR487z1_english.pdf",
            "answerable": True
        },
        {
            "query": "How many phases were involved in the iterative development process?",
            "language": "English",
            "type": "factual",
            "expected_source": "RAND_RR487z1_english.pdf",
            "answerable": True
        },
        {
            "query": "ما هو الفرق بين الخدمات الروتينية والبرامج المتخصصة؟",
            "language": "Arabic",
            "type": "complex",
            "expected_source": "RAND_RR1681z1.arabic.pdf",
            "answerable": True
        },
        {
            "query": "Who is the lead author mentioned in the citation for the 2008 report?",
            "language": "English",
            "type": "factual",
            "expected_source": "RAND_RR487z1_english.pdf",
            "answerable": True
        },
        {
            "query": "Does the report cover the impact of mental health on service members' families?",
            "language": "English",
            "type": "factual",
            "expected_source": "RAND_RR487z1_english.pdf",
            "answerable": True
        },
        {
            "query": "ما هي أهداف الفريق العامل المعني بالصحة العقلية في وزارة الدفاع؟",
            "language": "Arabic",
            "type": "factual",
            "expected_source": "RAND_RR1562z1.arabic.pdf",
            "answerable": True
        },
        {
            "query": "What does the abbreviation OSD stand for?",
            "language": "English",
            "type": "factual",
            "expected_source": "RAND_RR487z1_english.pdf",
            "answerable": True
        },
        {
            "query": "Is there any discussion about the use of blockchain in healthcare?",
            "language": "English",
            "type": "no-info",
            "expected_source": 0,
            "answerable": False
        },
        {
            "query": "كيف يتم تصنيف البرامج بناءً على 'التدخل' في أداة R-PCT؟",
            "language": "Arabic",
            "type": "complex",
            "expected_source": "RAND_RR487z1_english.pdf",
            "answerable": True
        },
        {
            "query": "Describe the data collection methods used for the catalog of programs.",
            "language": "English",
            "type": "complex",
            "expected_source": "RAND_RR487z1_english.pdf",
            "answerable": True
        },
        {
            "query": "ما هي العوائق التي واجهتها مؤسسة RAND عند تطوير الكتالوج؟",
            "language": "Arabic",
            "type": "factual",
            "expected_source": "RAND_RR1681z1.arabic.pdf",
            "answerable": True
        },
        {
            "query": "How many service members were estimated to have probable TBI by 2007?",
            "language": "English",
            "type": "factual",
            "expected_source": "RAND_RR487z1_english.pdf",
            "answerable": True
        },
        {
            "query": "Does the report suggest any policy changes for the VA?",
            "language": "English",
            "type": "complex",
            "expected_source": "RAND_RR487z1_english.pdf",
            "answerable": True
        },
        {
            "query": "هل هناك إشارة إلى مدن معينة في السعودية داخل التقرير؟",
            "language": "Arabic",
            "type": "no-info",
            "expected_source": 0,
            "answerable": False
        },
        {
            "query": "What is the primary goal of the R-PCT toolkit?",
            "language": "English",
            "type": "factual",
            "expected_source": "RAND_RR487z1_english.pdf",
            "answerable": True
        },
        {
            "query": "Explain the role of 'Expert Consultation' in the development of the tool.",
            "language": "English",
            "type": "complex",
            "expected_source": "RAND_RR487z1_english.pdf",
            "answerable": True
        },
        {
            "query": "ما هو العقد الذي تم بموجبه إجراء هذا البحث؟",
            "language": "Arabic",
            "type": "factual",
            "expected_source": "RAND_RR1562z1.arabic.pdf",
            "answerable": True
        },
        {
            "query": "How are 'Innovative Practices' defined within the context of the TBI program?",
            "language": "English",
            "type": "complex",
            "expected_source": "RAND_RR487z1_english.pdf",
            "answerable": True
        },
        {
            "query": "Does the report list the names of individual service members interviewed?",
            "language": "English",
            "type": "no-info",
            "expected_source": 0,
            "answerable": False
        },
        {
            "query": "ما هي الخطوات التالية المقترحة بعد تطوير أداة R-PCT؟",
            "language": "Arabic",
            "type": "complex",
            "expected_source": "RAND_RR1562z1.arabic.pdf",
            "answerable": True
        }
    ]
        
        return test_cases
