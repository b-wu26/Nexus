import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import { BACKEND_SERVER_DOMAIN } from '../../../settings'
import { v4 as uuidv4 } from 'uuid';
import { useSelector } from 'react-redux';



export default function CreatePost({ user, newPost, course_id }) {
    const [postText, setPostText] = useState("");
    const [courses, setCourses] = useState([]);
    const [selectedCourse, setSelectedCourse] = useState("");
    const [postFiles, setPostFiles] = useState([]);
    const [postFileName, setPostFileName] = useState("");

    const user_state = useSelector((state) => state.user); // Replace with your actual user ID
    const user_id = user_state.idstudent_profile;

    let btnRef = useRef();
    let postPictureBtnRef = useRef();
    let showBtn = useRef();
    let textAreaRef = useRef();
    const handlePostText = ({ target }) => {
        setPostText(target.value)
        textAreaRef.current.style.height = 'auto'
        textAreaRef.current.style.height = (textAreaRef.current.scrollHeight + 2) + 'px'
        if (target.value) {
            btnRef.current.removeAttribute("disabled");
            showBtn.current.classList.add("show-btn");
        } else {
            btnRef.current.setAttribute("disabled", "disabled");
        }
    };
    const clickPostPicture = () => {
        postPictureBtnRef.current.click();
    }

    const handleCourseChange = (event) => {
        setSelectedCourse(event.target.value);
    };

    const handlePostImageChange = (event) => {
        setPostFiles(event.target.files);
    };

    useEffect(() => {
        axios.get(`${BACKEND_SERVER_DOMAIN}/api/enrolled_courses/${user_id}`) // Replace with your actual API URL
            .then((response) => {
                setCourses(response.data.courses);
            })
            .catch((error) => {
                console.error(`Error fetching courses: ${error}`);
            });
    }, []);

    const handleSubmit = (event) => {
        event.preventDefault(); // Prevent the form from refreshing the page

        const formData = new FormData();
        formData.append('idposts', uuidv4());
        formData.append('idstudent_profile', user_id);
        if (course_id) {
            formData.append('idclass_profile', course_id);
        } else {
            formData.append('idclass_profile', selectedCourse);
        }
        formData.append('text_content', postText);
        formData.append('date_sent', new Date().toISOString());
        formData.append('upvotes', 0);
        formData.append('response_id', 0);
        formData.append('type', "posts");
        if (postFiles) {
            for (let i = 0; i < postFiles.length; i++) {
                formData.append('post_files', postFiles[i]);
                // console.log(postFiles[i]);
            }
        }

        if (course_id) {
            axios.post(`${BACKEND_SERVER_DOMAIN}/api/${user_id}/feed_post/${course_id}`, formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            }).then((response) => {
                console.log(response.data);
                newPost(response.data);
                setPostText("");
                setPostFiles([]);
                setPostFileName("");
                showBtn.current.classList.remove("show-btn");
            })
                .catch((error) => {
                    console.error(`Error creating post: ${error}`);
                });
            return;
        } else {
            axios.post(`${BACKEND_SERVER_DOMAIN}/api/${user_id}/feed_post/${selectedCourse}`, formData, {
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
        }

    };


    return (
        <section className="create-post">
            <h6>Start a discussion</h6>
            {!course_id ? (
                <div class="selectWrapper">
                    <select class="selectBox" value={selectedCourse} onChange={handleCourseChange}>
                        <option value="">Select a course</option>
                        {courses.map((course) => (
                            <option key={course.idclass_profile} value={course.idclass_profile}>{course.class_name}</option>
                        ))}
                    </select>
                </div>
            ) : null}
            <div className="d-flex">
                <img className="rounded-circle" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAOEAAADhCAMAAAAJbSJIAAAAPFBMVEXk5ueutLepsLPo6uursbXJzc/p6+zj5ea2u76orrKvtbi0ubzZ3N3O0dPAxcfg4uPMz9HU19i8wcPDx8qKXtGiAAAFTElEQVR4nO2d3XqzIAyAhUD916L3f6+f1m7tVvtNINFg8x5tZ32fQAIoMcsEQRAEQRAEQRAEQRAEQRAEQRAEQRAEQRAEQRAEQTghAJD1jWtnXJPP/54IgNzZQulSmxvTH6oYXX4WS+ivhTbqBa1r26cvCdCu6i0YXbdZ0o4A1rzV+5IcE3YE+z58T45lqo7g1Aa/JY5tgoqQF3qb382x7lNzBLcxft+O17QUYfQI4IIeklKsPSN4i6LKj/7Zm8n99RbHJpEw9gEBXNBpKIYLJqKYRwjOikf//r+J8ZsVuacbqCMNleI9TqGLGqMzhnVdBOdd6F/RlrFijiCoVMk320CBIahUxTWI0KKEcJqKbMdpdJb5QvdHq6wCI5qhKlgGMS/RBHkubWDAE+QZxB4xhCyDiDkLZxgGEVdQldzSKbTIhmZkFkSEPcVvmBn2SMuZB9od7fQDsMiDdKJjFUSCQarM5WirZ3C2TT/htYnyPcPfgrFHWz0BI74gr6J/IZiGUxAZGQLqmvQLTrtE/Go4YxhVRIpEw+sww1IIcqr5NKmUUzLF3d4/qPkYIp2T/obPuemlojFUR4t9Q2Vojhb7BmgElWHzLPH8hucfpefPNFTVgs9h1AdU/Pin96vwWbWdf+X9Absn3OdO34aMdsDnP8WgKYisTqI6CkNGqZQo1XA6Ef6AU32SJzOcBukHPF07/xNSgmHKa5BOhtezv6mA/rYJpwXNAnbRZ1XuF3BzDcO3vpA3+ny2909gbqE4hhD3LIPhLLyBNhPZvbZ3B+3tPYa18A7auSlXQayKwTPNLKDcuOB0xPYKDPFTkWsevQPRZ1J8Hji9I1KQ34r7hZhrwNwOZ97QxNx0drwn4QI0wQk1DcEsfKCWKdxVvxPSNUIp/knmAXT+nT+Ko3+0H96rcNb3m1fx7MBTJdeBJ7uFcWsc0wvgAsC4pROW0l2inbAmIBv/7GZmuhQH6API2rr8T0e6yuZJ+80A9LZeG62T3tik31XwxtwZcizKuTHkMjB1WdZde4Kmic/A5ZI3rr1ae21d08PlVHYfAaxw9G9CYRbJ+8ZdbTcMRV1XM3VdF0M32vtoTdZ0+u29s0OttJ5bz64UwinjaFMVY9vkqc3KKSxN21Xl+0L4Q3Vuv1tYl0pqnX6ms4XetFz7gdZVAgUEoJntfOUe4ZwsHd9FzqQ3Vv6xe41l0XJcqcKl6TZvlv7ClAW3BsqQW4X7ypApB8dmTgK4IX5wvqIVj33HtD2qSG4BqznxdIefL27Y4sahi0MdIdvUsDva8agGGbCtITmCY31MHD2O0uIdh/0rJDQ1VX5Zdxz3rR2QDbv6qXl9vudzqQtGm1Jv9LDXOsfvvB7VcZ8PDKD0mQ1VHPYQ9O+Yj4hR1IUD8rBnn3ho2m8oQMxbCFiKlL2ioSW5heeJqegED52CzxCtcGD3Kv8Wms9EYLyUhwaFIhSMBClevWEmiK/Iaogu4H7sg6ppQhQG8RUqivuTGOAJOg6FfgW0q0M0PQMRMEgXaeNf3SYDZ8PIMI0+wHgr/MgN7wYwpiLjCCqM6ydUDZLQiB6nDdNC8SDyig3jPPpFXGcC9O8BUBDVmgBY59E7Md/35Loe/UVEECEJwYggJjELZ4J71SaQSBeC02n4Da29CayJNA28SAhd2CQyC1Xw6pSmGSINQVuMhAZp4DClan9MgmkDDNmezqwS8sgtlXK/EPBhoaSmYVC/F7IO1jQEdHOlabpKh3+jzLQSTUiq4X2I+Ip/zU8rlaqAvkS21ElR+gqu3zbjjL+hIAiCIAiCIAiCIAiCsCf/AKrfVhSbvA+DAAAAAElFTkSuQmCC" alt="profile-picture" />
                <textarea ref={textAreaRef} placeholder="Enter text here" rows="1" onChange={handlePostText} name="post_text" value={postText}></textarea>
                <button onClick={clickPostPicture}><i className="far fa-file-image"></i></button>
            </div>
            <div className="submit-btn" ref={showBtn}>
                <button className="btn btn-primary btn-sm" type="submit" ref={btnRef} onClick={handleSubmit}>Submit</button>
            </div>
            <input type="file" accept="image/*,.pdf,.doc,.docx,.xls,.xlsx,.csv,.txt" name="post_file" ref={postPictureBtnRef} className="d-none" onChange={handlePostImageChange} multiple />            {postFiles.length > 0 &&
                <div className="files_to_be_uploaded">
                    <p>Files to be uploaded: {<br />}{Array.from(postFiles).map((file, index) => <span key={index}>{file.name}<br /></span>)}</p>
                </div>
            }
        </section>
    );
}
