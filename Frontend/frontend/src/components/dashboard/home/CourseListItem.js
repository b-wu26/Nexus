import React from 'react'
import { Link } from 'react-router-dom';


export default function CourseListItem({ course }) {

    return (
        <Link to={`/dashboard/${course.idclass_profile}`}>
            <div className="friendlistitem d-flex">
                <div>
                    <h6>{course.faculty} {course.course_code}: {course.class_name}</h6>
                </div>
            </div>
        </Link>
    );
}