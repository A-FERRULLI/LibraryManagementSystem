SELECT
    Students.name,
    Students.age,
    Students.gender
FROM
    Students
INNER JOIN
    Enrollments ON Students.student_id = Enrollments.student_id
INNER JOIN
    Courses ON Enrollments.course_id = Courses.course_id;

SELECT
    Students.name,
    Students.age,
    Students.gender
FROM
    Students
LEFT JOIN
    Enrollments ON Students.student_id = Enrollments.student_id
WHERE
    Enrollments.student_id IN NULL;

SELECT
    Courses.course_name,
    Courses.credits,
    Courses.capacity,
    COUNT(Enrollments.student_id) AS Enrolled
FROM
    Courses
LEFT JOIN
    Enrollments ON Courses.course_id = Enrollments.course_id
GROUP BY
    Courses.course_id;

SELECT
    Courses.course_name,
    Courses.credits,
    Courses.capacity,
    COUNT(Enrollments.student_id) AS Enrolled
FROM
    Courses
INNER JOIN
    Enrollments ON Courses.course_id = Enrollments.enrollment_id
GROUP BY
    Courses.course_id
HAVING
    COUNT(Enrolled.student_id) > Courses.capacity / 2;

SELECT
    Students.name,
    COUNT(Enrollments.course_id) AS Nb_Courses
FROM
    Students
INNER JOIN
    Enrollments ON Students.student_id = Enrollments.student_id
GROUP BY
    Students.student_id
HAVING
    COUNT(Enrollments.course_id) = (
        SELECT
            MAX(CourseCount)
        FROM (
            SELECT
                COUNT(Enrollments.course_id) AS CourseCount
            FROM
                Enrollments
            GROUP BY
                Enrollments.student_id
        ) AS Max_Courses
    );

SELECT 
    Students.name, 
    SUM(Courses.credits) AS TotalCredits
FROM 
    Students
INNER JOIN
    Enrollments ON Students.student_id = Enrollments.student_id
INNER JOIN
    Courses ON Enrollments.course_id = Courses.course_id
GROUP BY
    Students.student_id;

SELECT
    Courses.course_name
FROM
    Courses
LEFT JOIN
    Enrollments ON Courses.course_id = Enrollments.course_id
WHERE
    Enrollments.student_id IS NULL;

DELETE FROM
    Enrollments
WHERE
    Enrollments.course_id = 2;

DELETE
    Students
FROM
    Students
LEFT JOIN
    Enrollments ON Students.student_id = Enrollments.student_id
WHERE
    Enrollments.student_id IS NULL;
