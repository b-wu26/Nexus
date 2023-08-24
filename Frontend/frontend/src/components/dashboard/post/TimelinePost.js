import React, { useState, useRef, useEffect } from "react";
import { timeSince } from "../../../utils/timesince";
import { BACKEND_SERVER_DOMAIN } from "../../../settings";
import CommentComponent from "./Comment";
import axios from "axios";
import { Link } from 'react-router-dom';
import {getMetadata} from 'page-metadata-parser';
import { LazyLoadImage } from 'react-lazy-load-image-component';

const TimelinePost = ({ post }) => {
    const [isLiked, setIsLiked] = useState(false);
    const [likesCount, setLikesCount] = useState(0);
    const [comments, setComments] = useState();
    const [showComments, setShowComments] = useState(false);
    const [isLoadingComments,setIsLoadingComments] = useState(false);
    const [embedUrls,setEmbedUrls] = useState();
    const [isDeleted, setIsDeleted] = useState(false);
    let btnRef = useRef();

    const commentField = useRef();

    function splicedArray(array,index) {
        let nArr = [...array];
        nArr.splice(0,index+1);
        return nArr;
    }

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
                            id={"options"+post.id}
                            data-toggle="dropdown"
                            aria-haspopup="true"
                            aria-expanded="false"
                        >
                            <i className="fas fa-ellipsis-h"></i>
                        </button>
                        <div
                            className="dropdown-menu"
                            aria-labelledby={"options"+post.id}
                        >
                            <>option 1</>
                            <br/>
                            <>option 2</>
                        </div>
                    </div>
                </div>
            </div>
            <div>
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
            {post.post_image ? (
                <LazyLoadImage src={post.post_image} className="rounded post-picture" alt="" />
            ) : (
                ""
            )}
            <div className="d-flex post-actions">
                <button>
                    <i className="far fa-comment-alt"></i>{(comments) ? (comments.length == 0) ? "No " : comments.length +" " : ""}Comments
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
                    {likesCount > 0 ? likesCount+' ' : ''}Like
                    {likesCount > 1 ? "s" : ""}
                </button>
                <button>
                    <i className="far fa-share-square"></i>Share
                </button>
            </div>
            { (post.likes) ? 
                <div className="likedBy">Liked by&nbsp;
                        {post.likes.persons.slice(0,2).map((person, index)=> (
                            <span key={person.id}>
                                <Link to={"/u/"+person.slug} key={person.id}>
                                    {person.first_name} {person.last_name}
                                </Link>
                                {(post.likes.persons.length > 1 && index==0) ?", ":""}
                            </span>
                        ))} {(post.likes.persons.length > 2) ? " and "+(likesCount-2)+" others": ""}
                </div> : ""
            }
            <div className={(isLoadingComments) ? "slim-loading-bar":""}></div>
            
            {
                showComments && typeof comments == "object" ?
                    <div className="each-comment parent-comment">
                        {comments.slice().map((comment, index) => (
                            <div key={comment.id}>{(comment.comment_parent == 0) ?
                                    <CommentComponent 
                                        key={comment.id}
                                        comment={comment}
                                        user="Obama"
                                        allComments={splicedArray(comments,index)}/>
                            : ''}
                            {(Number(index+1) == Number(comments.length) && isLoadingComments) ? setIsLoadingComments(false) : ''}
                            </div>                       
                        ))}
                    </div>
                : <div></div>
            }
            <div className="post-comment">
                <div className="d-flex">
                    <input type="text" ref={commentField} placeholder="Write your comment..." />
                    <button>
                        <i className="far fa-paper-plane"></i>
                    </button>
                </div>
            </div>
        </article>
    );
};

export default TimelinePost;
