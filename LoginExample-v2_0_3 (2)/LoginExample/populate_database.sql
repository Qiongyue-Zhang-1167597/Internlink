USE InternLink;

-- Temporarily disable foreign key checks to allow truncation in any order
SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE `application`;
TRUNCATE TABLE `internship`;
TRUNCATE TABLE `student`;
TRUNCATE TABLE `employer`;
TRUNCATE TABLE `user`;
-- Re-enable foreign key checks
SET FOREIGN_KEY_CHECKS = 1;

-- --- Admins (2) ---
INSERT INTO `user` (`username`, `full_name`, `email`, `password_hash`, `role`, `status`) VALUES 
('admin_linda', 'Linda Stern', 'linda.stern@example.com', '$2b$12$AcBp6hO75Mt8Bh5fczsTxORsFjJnsJTiXVYw45nsoFiGJrk3n2ulq', 'admin', 'active'),
('admin_david', 'David Chen', 'david.chen@example.com', '$2b$12$1nVVpT7P2DNBy5cmtXToduXg0l.QcL5SBYWjEFfxkmXIEgDww5kV6', 'admin', 'active'),

-- --- Employers (5) ---
('techcorp', 'TechCorp Solutions', 'hr@techcorp.com', '$2b$12$uYEZxlo6jIfFaD24KzFCQOxG706x3Hl0uvfnQm8mjkKMfdp1WM7pO', 'employer', 'active'),
('innovate_inc', 'Innovate Inc.', 'careers@innovateinc.com', '$2b$12$vZ/B7JorQJEB74A9OlGeb.Wl469QVS29q0vJZKYPpabl7XP7qfMzy', 'employer', 'active'),
('datadigits', 'DataDigits Analytics', 'jobs@datadigits.com', '$2b$12$MJxvyKeZ5uD0AyOe4A2EUuRSqE7liZaDKNT7h0AQmtgRZ2Sn1jAz.', 'employer', 'active'),
('healthwell', 'HealthWell Partners', 'recruitment@healthwell.com', '$2b$12$Ir2aOMhZW8V2bWvkqIh8WOA2otewxOIh3INYDYHySnQu33TAcIopO', 'employer', 'active'),
('greenleaf', 'GreenLeaf Organics', 'apply@greenleaf.com', '$2b$12$a5XssD3zibqcqV.CYjgzFO6EjUsoNdFj7D0OGb7vWGiP7Pe78zBVW', 'employer', 'active'),

-- --- Students (20) ---
('janesmith', 'Jane Smith', 'jane.s@university.com', '$2b$12$KdHk96bzUT2WxMUzeAu0yebIdXh.LhXTPeyMN.AgGJM2FrVxMI6U6', 'student', 'active'),
('johndoe', 'John Doe', 'john.d@university.com', '$2b$12$rTp1WX5En8p5XfyNencHmOczJ6X5PGI65f9Kvt8QBYgshzHLeEMLe', 'student', 'active'),
('emilyjones', 'Emily Jones', 'emily.j@university.com', '$2b$12$AYaT4RDH7ERUVjR5dWbLs.GtzUmqNoP5NwQ4xAI2RR77ZRtMufx3i', 'student', 'active'),
('michaelw', 'Michael Williams', 'michael.w@university.com', '$2b$12$gDr2atuUDNKjQz0odTrUte1xtIbop0wrkP6kqbvebcWUlndRjyFHq', 'student', 'active'),
('sarahb', 'Sarah Brown', 'sarah.b@university.com', '$2b$12$am1IYxAxXdtdcHMxLHOMh.VGL5MQMQPTHTtUJ68Q7aOVdlqMrvgqq', 'student', 'active'),
('kevin_davis', 'Kevin Davis', 'kevin.d@university.com', '$2b$12$ZZOYYLpXKZz2z0Vp4vf54.BUkJGD2Ih89L8KrOKxv0xA.PbxDsMB.', 'student', 'active'),
('chloeg', 'Chloe Garcia', 'chloe.g@university.com', '$2b$12$HDPvcrmENuIqvre4UCr9be1oTGpHCbvsjueHQjPBg/2aWQEHFVsE6', 'student', 'active'),
('jamesr', 'James Rodriguez', 'james.r@university.com', '$2b$12$R7II3Ql1M2DIaaR2bIPoxOGsnsWxtoh8Hn/C0izHZrjPJedeI7psu', 'student', 'active'),
('olivia_m', 'Olivia Martinez', 'olivia.m@university.com', '$2b$12$qcSXtbul1Xlx7W7d4jyO7OXjqK4DOy1QovxC/MkA1MSRvxIA6Mg6O', 'student', 'active'),
('liam_h', 'Liam Hernandez', 'liam.h@university.com', '$2b$12$UZ8UDPD6bpapBKnPdXiebOnWDq5ngwsNtxSSG2fT9AgC0JecSfUjW', 'student', 'active'),
('ava_lopez', 'Ava Lopez', 'ava.l@university.com', '$2b$12$7m9wRjlD8ADt6m89PNmkjeGEeq/CqS4bV5Wm06iQz6hn6Lw2l6TAK', 'student', 'active'),
('noah_gonzalez', 'Noah Gonzalez', 'noah.g@university.com', '$2b$12$1VKkuhvtE0w1YWoxo7d0Ue2V/ZhvBCnwM.nchIe.s7Wpxnr0RcRRm', 'student', 'active'),
('isabella_p', 'Isabella Perez', 'isabella.p@university.com', '$2b$12$COOOfWq3YDAy/dh3WQPGzO4xod50EHrTn2NANDtzBzEvjjNsrOjim', 'student', 'active'),
('ethan_sanchez', 'Ethan Sanchez', 'ethan.s@university.com', '$2b$12$JoHCaWUqmrts6zGIZ3FFbOwJUQmaJrTXRvXlGf.tUHiI0Bctzg.9a', 'student', 'active'),
('sophia_rivera', 'Sophia Rivera', 'sophia.r@university.com', '$2b$12$gj3D0m2bPz6Lm5syHZku7OjtdE.mNAXnieZiWzVi2yBRaBo87I8Rq', 'student', 'active'),
('mason_t', 'Mason Torres', 'mason.t@university.com', '$2b$12$L9imbkN/vdCA0loiNMdHY.yUtGdzl9coXphETlDnU4.bb6Q4PnhPi', 'student', 'active'),
('mia_ramirez', 'Mia Ramirez', 'mia.r@university.com', '$2b$12$BzGPK3J.itMm463NkZ9OdetXImP5xYqBrbCYx9e1mHzT/PpPtkIey', 'student', 'active'),
('jacob_f', 'Jacob Flores', 'jacob.f@university.com', '$2b$12$Yp4pdRvElRT2D9o.ug/RkudeSwM509LjKK7yvpI80gzC4QzExoQtm', 'student', 'active'),
('charlotte_g', 'Charlotte Gomez', 'charlotte.g@university.com', '$2b$12$4Ysa/DNVuXtjRky8AiTL3uvUJ1XdbeLsTrxnoxLrlUrBAn8JwWqJa', 'student', 'active'),
('daniel_kim', 'Daniel Kim', 'daniel.k@university.com', '$2b$12$EmUBdT0NcZExOHeu9n4gBOcexljfmwJtJzy3eJY.q31q6lehiG4/e', 'student', 'active');


-- --- Employer Details ---
INSERT INTO `employer` (`emp_id`, `user_id`, `company_name`, `company_description`, `website`, `logo_path`) VALUES
(1, 3, 'TechCorp Solutions', 'A leading provider of enterprise software solutions.', 'https://techcorp.example.com', 'images/logos/techcorp.png'),
(2, 4, 'Innovate Inc.', 'Pioneering new technologies in the AI space.', 'https://innovateinc.example.com', 'images/logos/innovate.png'),
(3, 5, 'DataDigits Analytics', 'We turn data into actionable insights.', 'https://datadigits.example.com', 'images/logos/datadigits.png'),
(4, 6, 'HealthWell Partners', 'Revolutionizing healthcare with technology.', 'https://healthwell.example.com', 'images/logos/healthwell.png'),
(5, 7, 'GreenLeaf Organics', 'Sustainable solutions for a greener planet.', 'https://greenleaf.example.com', 'images/logos/greenleaf.png');

-- --- Student Details ---
INSERT INTO `student` (`student_id`, `user_id`, `university`, `course`, `resume_path`) VALUES
(1, 8, 'State University', 'Computer Science', 'resumes/janesmith_resume.pdf'),
(2, 9, 'City College', 'Software Engineering', 'resumes/johndoe_resume.pdf'),
(3, 10, 'Tech Institute', 'Data Science', 'resumes/emilyjones_resume.pdf'),
(4, 11, 'State University', 'Information Technology', 'resumes/michaelw_resume.pdf'),
(5, 12, 'Public University', 'Computer Science', 'resumes/sarahb_resume.pdf'),
(6, 13, 'City College', 'Cybersecurity', 'resumes/kevin_davis_resume.pdf'),
(7, 14, 'Tech Institute', 'AI and Machine Learning', 'resumes/chloeg_resume.pdf'),
(8, 15, 'State University', 'Web Development', 'resumes/jamesr_resume.pdf'),
(9, 16, 'Public University', 'Computer Engineering', 'resumes/olivia_m_resume.pdf'),
(10, 17, 'City College', 'Data Science', 'resumes/liam_h_resume.pdf'),
(11, 18, 'Tech Institute', 'Computer Science', 'resumes/ava_lopez_resume.pdf'),
(12, 19, 'State University', 'Software Engineering', 'resumes/noah_gonzalez_resume.pdf'),
(13, 20, 'Public University', 'Information Systems', 'resumes/isabella_p_resume.pdf'),
(14, 21, 'City College', 'Computer Science', 'resumes/ethan_sanchez_resume.pdf'),
(15, 22, 'Tech Institute', 'Cybersecurity', 'resumes/sophia_rivera_resume.pdf'),
(16, 23, 'State University', 'AI and Machine Learning', 'resumes/mason_t_resume.pdf'),
(17, 24, 'Public University', 'Web Development', 'resumes/mia_ramirez_resume.pdf'),
(18, 25, 'City College', 'Computer Engineering', 'resumes/jacob_f_resume.pdf'),
(19, 26, 'Tech Institute', 'Data Science', 'resumes/charlotte_g_resume.pdf'),
(20, 27, 'State University', 'Computer Science', 'resumes/daniel_kim_resume.pdf');


-- Populate `internship` table (20 Internships)
INSERT INTO `internship` (`internship_id`, `company_id`, `title`, `description`, `location`, `duration`, `skills_required`, `deadline`, `stipend`, `number_of_opening`, `additional_req`) VALUES
(1, 1, 'Junior Software Developer Intern', 'Work on our flagship enterprise software. Learn from senior developers.', 'New York, NY', '12 Weeks', 'Java, Spring, SQL', '2025-01-15', '$25/hr', 3, 'Must be pursuing a degree in Computer Science or related field.'),
(2, 2, 'AI Research Intern', 'Assist our R&D team in developing new machine learning models.', 'San Francisco, CA', '3 Months', 'Python, TensorFlow, PyTorch', '2025-01-20', '$35/hr', 2, 'Previous research experience is a plus.'),
(3, 3, 'Data Analyst Intern', 'Analyze large datasets to provide business insights.', 'Chicago, IL', '10 Weeks', 'SQL, Python, Pandas, Tableau', '2025-02-01', '$22/hr', 2, NULL),
(4, 4, 'Healthcare IT Intern', 'Support the development of our electronic health records system.', 'Boston, MA', 'Full Semester', 'Basic understanding of healthcare systems', '2025-01-25', 'Course Credit', 4, 'HIPAA training will be provided.'),
(5, 5, 'Marketing Intern (Tech)', 'Help market our new sustainable tech products.', 'Austin, TX', '12 Weeks', 'Social Media Marketing, SEO basics', '2025-02-05', '$20/hr', 1, NULL),
(6, 1, 'QA Tester Intern', 'Responsible for testing and quality assurance of our mobile applications.', 'New York, NY', '12 Weeks', 'Manual Testing, JIRA', '2025-01-18', '$20/hr', 3, 'Attention to detail is a must.'),
(7, 2, 'Frontend Developer Intern (React)', 'Build beautiful and responsive user interfaces with React.', 'Remote', '4 Months', 'HTML, CSS, JavaScript, React', '2025-02-10', '$30/hr', 2, 'Please provide a link to your portfolio or GitHub.'),
(8, 3, 'Business Intelligence Intern', 'Create dashboards and reports using tools like Tableau.', 'Chicago, IL', '10 Weeks', 'SQL, Excel, Power BI or Tableau', '2025-02-15', '$23/hr', 2, NULL),
(9, 4, 'Cybersecurity Intern', 'Monitor security alerts and assist with incident response.', 'Boston, MA', '3 Months', 'Networking basics, Linux', '2025-01-30', '$28/hr', 1, 'Interest in security is required.'),
(10, 5, 'Product Management Intern', 'Work with the product team to define features.', 'Austin, TX', '12 Weeks', 'Excellent communication skills', '2025-02-20', 'Unpaid', 1, 'This is a great opportunity to learn product lifecycle management.'),
(11, 1, 'Backend Developer Intern (Java)', 'Develop and maintain server-side logic for our core services.', 'Remote', '4 Months', 'Java, REST APIs, Git', '2025-02-01', '$32/hr', 2, NULL),
(12, 2, 'Machine Learning Engineer Intern', 'Implement and deploy ML models into production systems.', 'San Francisco, CA', '3 Months', 'Python, Docker, AWS/GCP', '2025-01-28', '$40/hr', 1, 'Strong background in algorithms and data structures.'),
(13, 3, 'Database Administrator Intern', 'Assist with the management and optimization of our MySQL databases.', 'Remote', '10 Weeks', 'MySQL, Database concepts', '2025-02-12', '$25/hr', 1, NULL),
(14, 1, 'DevOps Intern', 'Learn about CI/CD pipelines, Docker, and Kubernetes.', 'New York, NY', '12 Weeks', 'Linux, Shell Scripting', '2025-02-08', '$28/hr', 2, 'Passion for automation.'),
(15, 2, 'UX/UI Design Intern', 'Create wireframes, mockups, and prototypes for new app features.', 'San Francisco, CA', '3 Months', 'Figma, Sketch, Adobe XD', '2025-02-18', '$25/hr', 2, 'A strong portfolio is required.'),
(16, 4, 'Clinical Informatics Intern', 'Bridge the gap between clinical staff and IT projects.', 'Boston, MA', 'Full Semester', 'Interest in healthcare and technology', '2025-02-04', 'Course Credit', 3, NULL),
(17, 5, 'Supply Chain Analyst Intern', 'Analyze and improve the efficiency of our supply chain.', 'Austin, TX', '12 Weeks', 'Excel, Basic statistics', '2025-02-25', 'Unpaid', 1, NULL),
(18, 1, 'Cloud Engineer Intern (AWS)', 'Work with our cloud infrastructure team on AWS.', 'Remote', '4 Months', 'AWS (EC2, S3), Networking concepts', '2025-02-22', '$35/hr', 2, 'AWS certification is a plus, but not required.'),
(19, 2, 'Natural Language Processing Intern', 'Develop models for text analysis and understanding.', 'San Francisco, CA', '3 Months', 'Python, NLTK/spaCy', '2025-02-01', '$42/hr', 1, NULL),
(20, 3, 'Data Engineering Intern', 'Build and maintain data pipelines using ETL processes.', 'Chicago, IL', '10 Weeks', 'Python, SQL, Airflow (optional)', '2025-02-19', '$30/hr', 2, 'Familiarity with data warehousing concepts.');

-- Populate `application` table (20 Applications)
INSERT INTO `application` (`application_id`, `student_id`, `internship_id`, `status`, `feedback`) VALUES
(1, 1, 1, 'pending', NULL),
(2, 2, 2, 'pending', NULL),
(3, 3, 3, 'viewed', NULL),
(4, 4, 4, 'pending', NULL),
(5, 5, 5, 'shortlisted', 'The candidate has a strong portfolio. Proceeding to the interview stage.'),
(6, 6, 6, 'pending', NULL),
(7, 1, 7, 'rejected', 'Thank you for your application, but we have decided to move forward with other candidates whose experience better matches our needs at this time.'),
(8, 8, 8, 'pending', NULL),
(9, 9, 9, 'viewed', NULL),
(10, 10, 10, 'pending', NULL),
(11, 11, 11, 'pending', NULL),
(12, 12, 12, 'shortlisted', 'Excellent resume. Scheduling a technical screening.'),
(13, 13, 13, 'pending', NULL),
(14, 14, 14, 'accepted', 'Congratulations! We are pleased to offer you the internship position. An official offer letter will be sent to your email shortly.'),
(15, 15, 15, 'pending', NULL),
(16, 16, 16, 'rejected', 'While your qualifications are impressive, we have filled the position with another candidate.'),
(17, 17, 17, 'pending', NULL),
(18, 18, 18, 'viewed', NULL),
(19, 19, 19, 'pending', NULL),
(20, 20, 20, 'pending', NULL);

UPDATE internship 
SET category = 'IT' 
WHERE title LIKE '%Developer%' OR title LIKE '%Software%' OR title LIKE '%AWS%' OR title LIKE '%QA Tester%';

UPDATE internship 
SET category = 'Marketing' 
WHERE title LIKE '%Marketing%';

UPDATE internship 
SET category = 'Finance' 
WHERE title LIKE '%Analyst%';

UPDATE internship 
SET category = 'Human Resources' 
WHERE title LIKE '%HR%';

UPDATE internship SET category = 'Product' WHERE title LIKE '%Product Management%';
UPDATE internship SET category = 'Data' WHERE title LIKE '%Data Engineering%' OR title LIKE '%Business Intelligence%';
UPDATE internship SET category = 'Design' WHERE title LIKE '%UX/UI Design%';
UPDATE internship SET category = 'IT' WHERE title LIKE '%Database Administrator%' OR title LIKE '%DevOps%' OR title LIKE '%Cybersecurity%';
UPDATE internship SET category = 'Data' WHERE title LIKE '%Machine Learning%';

UPDATE internship SET category = 'Human Resources' WHERE title LIKE '%Clinical Informatics%' OR title LIKE '%Healthcare IT%';

UPDATE internship SET category = 'Data' WHERE title LIKE '%Natural Language Processing%' OR title LIKE '%AI Research%';

UPDATE internship SET category = 'IT' WHERE title LIKE '%QA Tester%';

SELECT 'Initial data populated successfully.' AS 'Status';