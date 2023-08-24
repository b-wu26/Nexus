import React, { useState, useEffect } from "react";
import { Link } from 'react-router-dom';

export default function Chat() {

    return (
        <div>
            <h6 className="mt-3">Live chat</h6>
            <div className="card friend-suggestions">
                <Room/>
                <Link className="card-btn">Create new room</Link>
            </div>
        </div>
    );
}

export function Room() {

    return (
        <div className="d-flex user">
            <div>
                <h6>
                    Chat room 1
                </h6>
                <span>Last active: 2 days ago</span>
                <button
                    className="btn btn-sm btn-outline-primary"
                >
                    Join room
                </button>
            </div>
        </div>
    )
}