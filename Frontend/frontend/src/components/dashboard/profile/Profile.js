import React from 'react'
import { Helmet } from "react-helmet";
import { useParams, Link } from 'react-router-dom';
import Navbar from "../Navbar";
import LeftSidebar from "../LeftSidebar";
import { useSelector } from 'react-redux';
import InputField from '../../../utils/InputField'

export default function Profile() {
    const {slug} = useParams();
    const user = useSelector((state) => state.user);
    const [tagline, setTagline] = React.useState("");
    const [home, setHome] = React.useState("");
    const [work, setWork] = React.useState("")

    let fakeCoverPictureBtnRef = React.useRef();
    let realCoverPictureBtnRef = React.useRef();
    let fakeProfilePictureBtnRef = React.useRef();
    let realProfilePictureBtnRef = React.useRef();

    React.useEffect(() => {
        window.scrollTo(0, 0);
    },[slug])

    return (
        <section className="profile-page">
            <Helmet>
                <title>First Last</title>
            </Helmet>
            <Navbar />
            <div className="navbar-spacer"></div>
            <div className="container">
                <div className="row">
                    <div className="col-lg-3 col-12">
                        <LeftSidebar />
                    </div>
                    <div className="col-lg-9 col-12 timeline">
                        <div>
                            <div className="card profile-user">
                                <div className="d-flex">
                                    <div className="user-details">
                                        <h6>First Last</h6>
                                        <p>University of Waterloo - 4th year ECE</p>
                                        {/* {(profileData.isFriend == false) ?
                                            (
                                                (profileData.isFriendReqSent == false) ?
                                                    (
                                                        <button className="btn btn-sm btn-primary" onClick={() => sendFriendReq(profileData.user.id)} ref={sendFriendReqBtn}>
                                                            <i className="fas fa-user-plus"></i> Send Friend Request
                                                        </button>
                                                    )
                                                : <button className="btn btn-sm btn-outline-primary" disabled="disabled">
                                                    <i className="fas fa-user-clock"></i> Friend Request Pending
                                                </button>
                                            ) : (profileData.isFriend == true) ?
                                            <button className="btn btn-sm btn-outline-success" disabled="disabled">
                                                <i className="fas fa-check"></i> Friends
                                            </button> : ""} */}
                                    </div> 
                                </div>  
                            </div>
                            <div className="row">
                                <div className="col-lg-8 col-md-12">
                                    <h6 className="ml-3 mt-1">Posts</h6>
                                    {/* <Posts key={1} token={user.token} userposts={profileData.posts.slice().reverse()} /> */}
                                </div>
                                <div className="col-lg-4 col-md-12 rightsidebar">
                                    <h6 className="ml-3">Recent Activity</h6>
                                    <div className="card">
                                        <div className="sorry-sm">No recent activities.</div>
                                    </div>
                                </div>
                            </div>

                            <div className="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
                            <div className="modal-dialog">
                                <div className="modal-content">
                                <div className="modal-body">
                                    <h5 className="mt-2 mb-2">Edit Profile</h5>
                                    <label className="form-label">Profile Picture&nbsp; <i className="far fa-file-image "></i></label>
                                    <button className="choose-avatar form-control" ref={fakeProfilePictureBtnRef}>
                                        choose profile picture
                                    </button>
                                    <input
                                        className="d-none"
                                        type="file"
                                        name="avatar"
                                        accept="image/*"
                                        ref={realProfilePictureBtnRef}
                                    />
                                    <label className="form-label">Cover Image&nbsp; <i className="far fa-file-image "></i></label>
                                    <button className="choose-avatar form-control" ref={fakeCoverPictureBtnRef}>
                                        choose cover image
                                    </button>
                                    <input
                                        className="d-none"
                                        type="file"
                                        name="cover"
                                        accept="image/*"
                                        ref={realCoverPictureBtnRef}
                                    />
                                    <InputField
                                        type="text"
                                        name="tagline"
                                        label="Tagline"
                                        value={tagline}
                                        />
                                    <InputField
                                        type="text"
                                        name="work"
                                        label="Work"
                                        value={work}
                                        />
                                    <InputField
                                        type="text"
                                        name="hometown"
                                        label="Hometown"
                                        value={home}
                                        />
                                </div>
                                <div className="modal-footer">
                                    <button type="button" className="btn btn-secondary" data-dismiss="modal">Close</button>
                                    <button type="button" className="btn btn-primary">Save changes</button>
                                </div>
                                </div>
                            </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    )
}