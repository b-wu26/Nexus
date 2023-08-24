import React, { useState, useEffect } from "react";

export default function About() {

    return (
        <div>
            <h6 className="mt-3">About course</h6>
            <div className="friend-req card">
                <CourseDescription/>
            </div>
        </div>
    );
}

export function CourseDescription() {

    let acceptBtn = React.useRef();
    let declineBtn = React.useRef();

    return (
        <div className="d-flex user">
            <img
                className="rounded-circle"
                src="https://upload.wikimedia.org/wikipedia/en/thumb/6/6e/University_of_Waterloo_seal.svg/1200px-University_of_Waterloo_seal.svg.png"
                alt="profile picture"
            />
            <div>
                <h6>
                    ECE 498A
                </h6>
                <span>Spring 2023</span>
                <div className="d-flex">
                    <button
                        ref={acceptBtn}
                        className="btn btn-sm btn-outline-primary"
                    >
                        Invite
                    </button> 
                    <button
                        ref={declineBtn}
                        className="btn btn-sm btn-outline-danger"
                    >
                        Leave
                    </button>
                </div>
            </div>
        </div>
    )
}
