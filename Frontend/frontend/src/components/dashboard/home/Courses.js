import React, { useState, useEffect } from "react";
import { Helmet } from "react-helmet";
import LeftSidebar from "../LeftSidebar";
import CourseListItem from "./CourseListItem";
import Navbar from "../Navbar";
import axios from 'axios';
import { BACKEND_SERVER_DOMAIN } from '../../../settings'

const user_id = 1; // Replace with your actual user ID

export default function Courses() {
    const course = [{ name: "ECE 455" },
    { name: "ECE 458" },
    { name: "ECE 498A" },
    { name: "MSCI 331" },
    { name: "MATH 115" }]

    const [courses, setCourses] = useState({});

    useEffect(() => {
        axios.get(`${BACKEND_SERVER_DOMAIN}/api/enrolled_courses/${user_id}`) // Replace with your actual API URL
            .then((response) => {
                const coursesByFaculty = response.data.courses.reduce((groups, course) => {
                    const faculty = course.faculty;
                    if (!groups[faculty]) {
                        groups[faculty] = [];
                    }
                    groups[faculty].push(course);
                    return groups;
                }, {});
                setCourses(coursesByFaculty);
                console.log(coursesByFaculty);
            })
            .catch((error) => {
                console.error(`Error fetching courses: ${error}`);
            });
    }, []);


    return (
        <section className="friends">
            <Helmet>
                <title>My Courses</title>
            </Helmet>
            <Navbar />
            <div className="navbar-spacer"></div>
            <div className="container">
                <div className="row">
                    <div className="col-lg-3 col-12">
                        <LeftSidebar active={2} />
                    </div>
                    <div className="col-lg-6 col-12 timeline">
                        {Object.entries(courses).map(([faculty, courses]) => (
                            <div key={faculty}>
                                <h6 className="mt-3">{faculty}</h6>
                                <div class="card">
                                    <div className="friends-list">
                                        {courses.map((course) => (
                                            <CourseListItem key={course.idclass_profile} course={course} />
                                        ))}
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </section>
    );
}
