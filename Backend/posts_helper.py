from models.student_profile import student_profile
from models.class_profile import class_profile

def create_posts(posts):

    data = []
    for post in posts:
    
        poster_profile = student_profile.get_student_by_id(post.idstudent_profile)
        course = class_profile.get_class_by_id(post.idclass_profile)
        data.append({"id": post.idposts,
            "poster": {"first": poster_profile.f_name, "last": poster_profile.l_name},
            "course": {"name": course.class_name, "code": course.course_code},
            "pfp": "",
            "created": post.date_sent,
            "post_text": post.text_content
        })

    return data