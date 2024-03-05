import React, { useState, useEffect } from "react";
import { Link } from 'react-router-dom';
import { useSelector } from 'react-redux';
import { BACKEND_SERVER_DOMAIN } from '../../../settings'
import axios from 'axios';

export default function Chat(props) {

    return (
        <div>
            <h6 className="mt-3">Live chat</h6>
            <div className="card friend-suggestions">
                <Room course_id={props.course_id} />
            </div>
        </div>
    );
}

export function Room(props) {
    const user_id = useSelector((state) => state.user).idstudent_profile;
    const [lastActive, setLastActive] = useState('');

    useEffect(() => {
        axios.get(`${BACKEND_SERVER_DOMAIN}/api/courses/course/${props.course_id}`)
            .then((response) => {
                console.log(response.data);
                setLastActive(response.data.courses.lastActive);
            })
            .catch((error) => {
                setLastActive('Unknown');
                console.error(`Error fetching last active: ${error}`);
            });
    }, []);

    return (
        <div className="d-flex user">
            <div>
                <h6>
                    Chat room
                </h6>
                <span>Last active: {lastActive}</span>
                <button
                    className="btn btn-sm btn-outline-primary"
                    onClick={() => {
                        const newWindow = window.open(`/chat/${user_id}/${props.course_id}`, '_blank');
                        if (newWindow) {
                            newWindow.focus();

                            axios.get(`${BACKEND_SERVER_DOMAIN}/chat/${user_id}/${props.course_id}`)
                                .then(function (response) {
                                    newWindow.document.write(response.data);
                                    newWindow.document.close();
                                })
                                .catch(function (error) {
                                    console.log(error);
                                });
                        }
                    }}
                >
                    Open chat
                </button>
            </div>
        </div>
    )
}