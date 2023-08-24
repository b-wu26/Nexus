import React from "react";
import { Helmet } from "react-helmet";
import LeftSidebar from "../LeftSidebar";
import CourseListItem from "./CourseListItem";
import Navbar from "../Navbar";

export default function Courses() {
    const course = [{name: "ECE 455"},
                    {name: "ECE 458"},
                    {name: "ECE 498A"},
                    {name: "MSCI 331"},
                    {name: "MATH 115"}]

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
                        <LeftSidebar active={2}/>
                    </div>
                    <div className="col-lg-6 col-12 timeline">
                        <h6 className="mt-3">ECE</h6>
                        <div class="card">
                            <div className="friends-list">
                                <CourseListItem course={course[0]} />
                                <CourseListItem course={course[1]} />
                                <CourseListItem course={course[2]} />
                            </div>
                        </div>
                        <h6 className="mt-3">MATH</h6>
                        <div class="card">
                            <div className="friends-list">
                                <CourseListItem course={course[4]} />
                            </div>
                        </div>
                        <h6 className="mt-3">MSCI</h6>
                        <div class="card">
                            <div className="friends-list">
                                <CourseListItem course={course[3]} />
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    );
}
