import React from 'react'
import { Helmet } from "react-helmet";
import { useParams, Link } from 'react-router-dom';
import Navbar from "../Navbar";
import LeftSidebar from "../LeftSidebar";
import { useSelector } from 'react-redux';
import InputField from '../../../utils/InputField'
import { BACKEND_SERVER_DOMAIN } from '../../../settings'
import axios from "axios";
import InfoPopup from './InfoPopup';
import './Profile.css'

export default function Profile() {
    const { slug } = useParams();
    const [tagline, setTagline] = React.useState("");
    const [home, setHome] = React.useState("");
    const [work, setWork] = React.useState("")
    const [info, setInfo] = React.useState([]);
    const [profPic, setProfPic] = React.useState([]);
    const [buttonPopup, setButtonPopup] = React.useState(false)

    const user = useSelector((state) => state.user); // Replace with your actual user ID
    const user_id = user.idstudent_profile;

    let fakeCoverPictureBtnRef = React.useRef();
    let realCoverPictureBtnRef = React.useRef();
    let fakeProfilePictureBtnRef = React.useRef();
    let realProfilePictureBtnRef = React.useRef();
    let postPictureBtnRef = React.useRef();

    React.useEffect(() => {
        window.scrollTo(0, 0);
        axios.get(`${BACKEND_SERVER_DOMAIN}/api/user_info/${user_id}`) // Replace with your actual API URL
            .then((response) => {
                setInfo(response.data);
            })
            .catch((error) => {
                console.error(`Error fetching courses: ${error}`);
            });
    }, [slug])

    const handlePostImageChange = (event) => {
        setProfPic(event.target.files);
    };

    const clickPostPicture = () => {
        postPictureBtnRef.current.click();
    }

    const handleSubmit = () => {
        setButtonPopup(false)

        //reference handleSubmit in CreatePost.js
        const formData = new FormData();
        formData.append('idstudent_profile', user_id);
        formData.append('bio', document.getElementById("bio").value);
        formData.append('major', document.getElementById("major").value);
        if (document.getElementById("term").value === "value") {
            formData.append('term', "");
            console.log("Error checking works");
        }
        else {
            formData.append('term', document.getElementById("term").value);
        }

        for (const pair of formData.entries()) {
            console.log(pair[0], pair[1]);
        }
        if (profPic) {
            for (let i = 0; i < profPic.length; i++) {
                formData.append('post_files', profPic[i]);
            }
        }

        axios.put(`${BACKEND_SERVER_DOMAIN}/api/user_info/${user_id}`, formData, {
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
        // axios.post(`${BACKEND_SERVER_DOMAIN}/api/user_info/${user_id}`, bioUpdate)
    }

    const renderClassCard = (card, index) => {
        return (
            <div class="card" key={index}>
                 <Link to={`/dashboard/${card.idclass_profile}`}>
                    <div class="card-body">
                        <h5 class="card-title">{card.course_code}</h5>
                        <h6 class="card-subtitle mb-2 text-body-secondary">{card.class_name}</h6>
                    </div>
                </Link>
            </div>
        )
    }

    const renderPostCard = (card, index) => {
        return (
            <div class="card" key={index}>
                <Link to={`/dashboard/${card.idclass_profile}`}>
                    <div class="card-body">
                        <h8 class="card-text">{card.text_content}</h8>
                        <h6 class="card-subtitle mb-2 text-body-secondary">{card.class_name}</h6>
                        <h5 class="card-title">{card.course_code}</h5>
                    </div>
                </Link>
            </div>

        )
    }

    //way to apparently force axios to load the data since profile needs db info to actually do stuff
    if (!info || !info.info) {
        return null;
    }
    console.log(info)
    const status = (info.info.major && info.info.term) ? `${info.info.term} ${info.info.major} Student` : "University of Waterloo Student";
    const bio = info.info.bio ? info.info.bio : "Tell us about yourself!";
    const name = info.info.first ? `${info.info.first} ${info.info.last}` : "First Last";
    console.log("NAME")
    console.log(name)

    if (!info) {
        return null;
    }
    return (
        <section className="profile-page">
            <Helmet>
                <title>Nexus</title>
            </Helmet>
            <Navbar />
            <InfoPopup trigger={buttonPopup} setTrigger={setButtonPopup}>
                <div>
                    <h3>Edit Personal Info</h3>
                    <br></br>
                    <input type="text" id="bio" placeholder="About me"></input>
                    <br></br>
                    <input type="text" id="major" placeholder='Major'></input>
                    <br></br>
                    <select name="term" id="term">
                        <option value="value" selected>Select Term</option>
                        <option value="1A">1A</option>
                        <option value="1B">1B</option>
                        <option value="2A">2A</option>
                        <option value="2B">2B</option>
                        <option value="3A">3A</option>
                        <option value="3B">3B</option>
                        <option value="4A">4A</option>
                        <option value="4B">4B</option>
                        <option value="Grad">Post-Grad</option>
                    </select>
                    <br></br>
                    <button onClick={clickPostPicture}><i className="far fa-file-image"></i></button>
                    <input type="file" accept="image/*" name="post_file" ref={postPictureBtnRef} className="d-none" onChange={handlePostImageChange} />            {profPic.length > 0 &&
                        <div className="files_to_be_uploaded">
                            <p>Files to be uploaded: {<br />}{Array.from(profPic).map((file, index) => <span key={index}>{file.name}<br /></span>)}</p>
                        </div>
                    }
                    <button className='submit-btn' onClick={handleSubmit}>
                        Submit
                    </button>
                </div>
            </InfoPopup>
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
                                        <h6>{name}</h6>
                                        <h7>{status}</h7>
                                        <p>{bio}</p>
                                        <button className="btn btn-sm btn-primary" onClick={() => setButtonPopup(true)}>Edit</button>

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
                                    <h6 className="ml-3 mt-1">Classes This Term</h6>
                                    {info.classes.map(renderClassCard)}
                                    {/* <Posts key={1} token={user.token} userposts={profileData.posts.slice().reverse()} /> */}

                                    <h6></h6>
                                </div>
                                <div className="col-lg-4 col-md-12 rightsidebar">
                                    <h6 className="ml-3">Recent Activity</h6>
                                    {/* <div className="card">
                                        <div className="sorry-sm">No recent activities.</div>
                                    </div> */}
                                    {info.posts.map(renderPostCard)}
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