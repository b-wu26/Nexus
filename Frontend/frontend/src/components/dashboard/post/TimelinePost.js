import React, { useState, useRef, useEffect } from "react";
import { timeSince } from "../../../utils/timesince";
import { BACKEND_SERVER_DOMAIN } from "../../../settings";
import CommentComponent from "./Comment";
import axios from "axios";
import { Link } from 'react-router-dom';
import { getMetadata } from 'page-metadata-parser';
import { LazyLoadImage } from 'react-lazy-load-image-component';
import ImageSlider from './ImageSlider';


const user_id = 1; // Replace with your actual user ID

const TimelinePost = ({ post }) => {
    const [isLiked, setIsLiked] = useState(false);
    const [likesCount, setLikesCount] = useState(0);
    const [comments, setComments] = useState();
    const [showComments, setShowComments] = useState(true);
    const [isLoadingComments, setIsLoadingComments] = useState(false);
    const [embedUrls, setEmbedUrls] = useState();
    const [isDeleted, setIsDeleted] = useState(false);
    const [postFiles, setPostFiles] = useState([]);
    let postPictureBtnRef = useRef();
    const [numCommentsToShow, setNumCommentsToShow] = useState(3);
    const [areCommentsShown, setAreCommentsShown] = useState(true);


    let btnRef = useRef();

    console.log("comments: ");
    console.log(post.comments);

    // function splicedArray(array, index) {
    //     let nArr = [...array];
    //     nArr.splice(0, index + 1);
    //     return nArr;
    // }

    const commentField = useRef(null);

    const clickPostPicture = () => {
        postPictureBtnRef.current.click();
    }

    const handlePostImageChange = (event) => {
        setPostFiles(event.target.files);
    };

    const handleSubmit = (event) => {
        event.preventDefault(); // Prevent the form from refreshing the page

        const formData = new FormData();
        formData.append('comment', commentField.current.value);
        formData.append('date_sent', new Date().toISOString());
        if (postFiles) {
            for (let i = 0; i < postFiles.length; i++) {
                formData.append('post_files', postFiles[i]);
                console.log(postFiles[i]);
            }
        }

        axios.post(`${BACKEND_SERVER_DOMAIN}/api/${user_id}/comment/${post.id}`, formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        }).then((response) => {
            console.log(response.data);
            window.location.reload();
        })
            .catch((error) => {
                console.error(`Error creating post: ${error}`);
            });
    };

    return (
        <article className="post card">
            <div className="d-flex userbar">
                <LazyLoadImage
                    loading="lazy"
                    className="rounded-circle"
                    src={post.pfp}
                    alt=""
                />
                <div>
                    <h6>
                        {post.poster.first} {post.poster.last}
                    </h6>
                    <span>{post.created}</span>
                </div>
                <div className="more-options">
                    <div className="dropleft">
                        <button
                            className="post-actions"
                            type="button"
                            id={"options" + post.id}
                            data-toggle="dropdown"
                            aria-haspopup="true"
                            aria-expanded="false"
                        >
                            <i className="fas fa-ellipsis-h"></i>
                        </button>
                        <div
                            className="dropdown-menu"
                            aria-labelledby={"options" + post.id}
                        >
                            <>Delete</>
                            <br />
                            <>Edit</>
                        </div>
                    </div>
                </div>
            </div>
            <div>
                <p>{post.course.code} : {post.course.name}</p>
                <p className="post-content">{post.post_text}</p>
                {(embedUrls) ? (embedUrls.map((url, index) => (
                    <a className="url" href={url.url} key={index} target="_blank">
                        <div>
                            <div className="utitle"><i className="fas fa-external-link-alt"></i> {url.title}</div>
                            {(url.description) ? <div className="udescription">{url.description}</div> : ""}
                            <div className="uurl">{url.url}</div>
                        </div>
                    </a>
                ))) : ""}
            </div>
            {post.attachments.images.length > 0 &&
                <div style={{ width: '100%' }} >
                    <ImageSlider images={post.attachments.images} />
                </div>
            }
            {post.attachments.files.length > 0 &&
                <div style={{ width: '100%', marginTop: '20px' }} >
                    <p><strong>File Attachments:</strong></p>
                    {post.attachments.files.map((file, index) => {
                        const fileName = file.split("/").pop();
                        return (
                            <a key={index} href={file} download>
                                <i className="fas fa-file"></i> {fileName}
                            </a>
                        );
                    })}
                </div>
            }
            <div className="d-flex post-actions">
                <button>
                    <i className="far fa-comment-alt"></i>{(comments) ? (comments.length == 0) ? "No " : comments.length + " " : ""}Comments
                </button>
                <button
                    ref={btnRef}
                    className={
                        isLiked
                            ? "btn btn-light btn-light-accent"
                            : "btn btn-light"
                    }
                >
                    <i className="far fa-thumbs-up"></i>
                    {likesCount > 0 ? likesCount + ' ' : ''}Like
                    {likesCount > 1 ? "s" : ""}
                </button>
                <button>
                    <i className="far fa-share-square"></i>Share
                </button>
            </div>
            {
                (post.likes) ?
                    <div className="likedBy">Liked by&nbsp;
                        {post.likes.persons.slice(0, 2).map((person, index) => (
                            <span key={person.id}>
                                <Link to={"/u/" + person.slug} key={person.id}>
                                    {person.first_name} {person.last_name}
                                </Link>
                                {(post.likes.persons.length > 1 && index == 0) ? ", " : ""}
                            </span>
                        ))} {(post.likes.persons.length > 2) ? " and " + (likesCount - 2) + " others" : ""}
                    </div> : ""
            }
            <div className={(isLoadingComments) ? "slim-loading-bar" : ""}></div>

            {
                <div className="each-comment parent-comment">
                    {areCommentsShown && post.comments.slice(0, numCommentsToShow).map((comment, index) => (
                        <div key={comment.id}>
                            < CommentComponent
                                comment={comment}
                            />
                            {(Number(index + 1) == Number(post.comments.length) && isLoadingComments) ? setIsLoadingComments(false) : ''}
                        </div>
                    ))}
                    {post.comments.length > numCommentsToShow &&
                        <button className="comment-show-more-button" onClick={() => setNumCommentsToShow(numCommentsToShow + 3)}>Show More</button>
                    }
                    {areCommentsShown && numCommentsToShow > 3 &&
                        <button className="comment-show-more-button" onClick={() => { setNumCommentsToShow(numCommentsToShow - 3); }}>Hide Comments</button>
                    }
                    {!areCommentsShown &&
                        <button className="comment-show-more-button" onClick={() => setAreCommentsShown(true)}>Show Comments</button>
                    }
                </div>
            }

            <div className="post-comment">
                <div className="d-flex">
                    <input type="text" ref={commentField} placeholder="Write your comment..." />
                    <button onClick={clickPostPicture}><i className="far fa-file-image"></i></button>

                    <input type="file" accept="image/*,.pdf,.doc,.docx,.xls,.xlsx,.csv,.txt" name="post_file" ref={postPictureBtnRef} className="d-none" onChange={handlePostImageChange} multiple />            {postFiles.length > 0 &&
                        <div className="files_to_be_uploaded">
                            <p>Files to be uploaded: {<br />}{Array.from(postFiles).map((file, index) => <span key={index}>{file.name}<br /></span>)}</p>
                        </div>
                    }
                    <button onClick={handleSubmit}>
                        <i className="far fa-paper-plane"></i>
                    </button>


                </div>

            </div>
        </article >
    );
};

export default TimelinePost;
