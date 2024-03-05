import React, { useState, useEffect } from "react";
import axios from "axios";
import { BACKEND_SERVER_DOMAIN } from '../../../settings'
import { useSelector } from 'react-redux';

export default function About(props) {
    // console.log("About", props.course_id)
    return (
        <div>
            <h6 className="mt-3">About course</h6>
            <div className="friend-req card">
                <CourseDescription course_id={props.course_id} />
            </div>
        </div>
    );
}

export function CourseDescription(props) {

    let acceptBtn = React.useRef();
    let declineBtn = React.useRef();
    let inviteBtn = React.useRef();
    const [courseInfo, setInfo] = React.useState([]);
    const [schedule, setSchedule] = React.useState([]);
    // console.log("here", props.course_id)
    const course_id = props.course_id
    const user = useSelector((state) => state.user);
    const user_id = user.idstudent_profile;

    const date = new Date();
    const month = date.getMonth() + 1;
    const year = date.getFullYear();
    let term = ""
    if (month < 5) {
        term = `Winter ${year}`
    } else if (month < 9) {
        term = `Spring ${year}`
    } else {
        term = `Fall ${year}`
    }

    const [enrolled, setEnrolled] = React.useState(null);

    React.useEffect(() => {
        window.scrollTo(0, 0);
        axios.get(`${BACKEND_SERVER_DOMAIN}/api/courses/course/${course_id}`) // Replace with your actual API URL
            .then((response) => {
                setInfo(response.data);
            })
            .catch((error) => {
                console.error(`Error fetching courses: ${error}`);
            });

    }, [])

    React.useEffect(() => {
        axios.get(`${BACKEND_SERVER_DOMAIN}/api/user_info/subscribe/${user_id}/${course_id}`)
            .then((response) => {
                setEnrolled(response.data["response"] === "subscribed");
            })
            .catch((error) => {
                console.error(`Error fetching courses: ${error}`);
            });
    }, [])

    const addCourse = () => {
        const formData = new FormData();
        formData.append('idstudent_profile', user_id);
        formData.append('idclass_profile', course_id);

        for (const pair of formData.entries()) {
            console.log(pair[0], pair[1]);
        }

        axios.post(`${BACKEND_SERVER_DOMAIN}/api/user_info/subscribe/${user_id}/${course_id}`, formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        }).then((response) => {
            console.log(response.data);
            window.location.reload();
        }).catch((error) => {
            console.error(`Error creating post: ${error}`);
        });
        console.log(formData);
        setEnrolled(true);
    }

    const deleteCourse = () => {
        console.log("ATTEMPTING DELETE")
        const formData = new FormData();
        formData.append('idstudent_profile', user_id);
        formData.append('idclass_profile', course_id);

        // for (const pair of formData.entries()) {
        //     console.log(pair[0], pair[1]);
        // }

        axios.delete(`${BACKEND_SERVER_DOMAIN}/api/user_info/subscribe/${user_id}/${course_id}`, formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        }).then((response) => {
            console.log(response.data);
            window.location.reload();
        }).catch((error) => {
            console.error(`Error creating post: ${error}`);
        });
        setEnrolled(false);
    }


    if (!courseInfo) {
        return null;
    }

    const name = courseInfo.courses ? `${courseInfo.courses.class_name} ` : "Course name";
    // console.log("class profile",courseInfo)
    return (
        <div className="d-flex user">
            <img
                className="rounded-circle"
                src="https://upload.wikimedia.org/wikipedia/en/thumb/6/6e/University_of_Waterloo_seal.svg/1200px-University_of_Waterloo_seal.svg.png"
                alt="profile picture"
            />
            <div>
                <h6>
                    {name}
                </h6>
                <span>{term}</span>
                <div className="d-flex">
                    {enrolled ? (
                        <button
                            onClick={deleteCourse}
                            className="btn btn-sm btn-outline-danger"
                        >
                            Leave
                        </button>
                    ) : (
                        <button
                            onClick={addCourse}
                            className="btn btn-sm btn-outline-primary"
                        >
                            Add
                        </button>
                    )}
                </div>
            </div>
        </div>
    )
}
