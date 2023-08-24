import React from 'react'
import { BACKEND_SERVER_DOMAIN } from "../../../settings";
import { Link } from "react-router-dom";

export default function CourseListItem({course}) {

    return (
        <div className="friendlistitem d-flex">
            <div>
                <h6>{course.name}</h6>
            </div>
        </div>
    );
}