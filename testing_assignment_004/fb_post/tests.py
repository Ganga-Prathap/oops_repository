from django.test import TestCase
import pytest
# Create your tests here.
from . utils import *

from freezegun import freeze_time
import datetime
import unittest
from django.utils import *


@pytest.fixture
def user():
    
    User.objects.bulk_create([
        User( name = 'Prathap' ),
        User( name = 'Sagaram' ),
        User( name = 'Rajesh' ),
        User( name = 'Naveen' ),
    ])


@pytest.fixture
@freeze_time("2020-04-18")
def post(user):
    
    Post.objects.bulk_create([
        Post(
            content = 'Good morning', 
            posted_by_id = 1
        ),
        Post(
            content = 'hello', 
            posted_by_id = 2
        ),
        Post(
            content = 'say hai', 
            posted_by_id = 4
        )
    ])
    
    
@pytest.fixture
@freeze_time("2020-04-18")
def comment(user, post):
    
    Comment.objects.bulk_create([
        Comment(
            content = 'nice', 
            commented_by_id = 2, 
            post_id = 1
        ),    
        Comment(
            content = 'ohh', 
            commented_by_id = 3, 
            post_id = 1
        ),
        Comment(
            content = 'ahaa', 
            commented_by_id = 1, 
            post_id = 2
        ),
    ])
    

@pytest.fixture
@freeze_time("2020-04-18")
def replycomment(user, post, comment):
    
    Comment.objects.bulk_create([
        Comment(
            content = 'thanks', 
            commented_by_id = 1, 
            post_id = 1, 
            parent_comment_id = 1
        ),    
        Comment(
            content = 'haa', 
            commented_by_id = 1, 
            post_id = 1, 
            parent_comment_id = 2
        ),
    ])
    

@pytest.fixture
def reactpost(user, post):
    
    Reaction.objects.bulk_create([
        Reaction(
            post_id = 1, 
            reaction = ReactionEnum.WOW.value, 
            reacted_by_id = 3
        ),
        Reaction(
            post_id = 2, 
            reaction = ReactionEnum.LOVE.value, 
            reacted_by_id = 1
        ),
        Reaction(
            post_id = 1, 
            reaction = ReactionEnum.THUMBSDOWN.value, 
            reacted_by_id = 2
        ),
        Reaction(
            post_id = 2, 
            reaction = ReactionEnum.SAD.value, 
            reacted_by_id = 3
        ),
        Reaction(
            post_id = 1, 
            reaction = ReactionEnum.LOVE.value, 
            reacted_by_id = 1
        ),
        Reaction(
            post_id = 3, 
            reaction = ReactionEnum.ANGRY.value, 
            reacted_by_id = 3
        ),
    ])
    
    
@pytest.fixture
def reactcomment(user, post, comment, replycomment):
    
    Reaction.objects.bulk_create([
        Reaction(
            comment_id = 1, 
            reaction = ReactionEnum.THUMBSUP.value, 
            reacted_by_id = 1
        ),
        Reaction(
            comment_id = 3, 
            reaction = ReactionEnum.WOW.value, 
            reacted_by_id = 2
        ),
        Reaction(
            comment_id = 4, 
            reaction = ReactionEnum.LIT.value, 
            reacted_by_id = 2
        ),
    ])


# TODO: Make necessary changes
@pytest.mark.django_db
@freeze_time("2020-04-17")
class TestCreatePosts:
    
    pytestmark = pytest.mark.django_db
    
    def test_create_post_with_valid_details_return_post_id(
        self, user):
        
        # Arrange
        user_id = 1
        post_content = "hello"
        
        # Act
        post_id = create_post(
            user_id, 
            post_content
        )
        
        # Assert
        post = Post.objects.get(id = post_id)
        
        assert post.posted_by_id == user_id
        assert post.content == post_content
        assert post.posted_at == timezone.now()
        

    def test_create_post_with_invalid_user_id_raise_error(self):
        
        # Arrange
        user_id = 1
        post_content = "hello"
        
        # Act
        with pytest.raises(InvalidUserException):
            create_post(
                user_id, 
                post_content
            )
            
        # Assert
      
        
    def test_create_post_with_invalid_post_content_raise_error(
        self, user):
        
        # Arrange
        user_id = 1
        post_content = ""
        
        # Act
        with pytest.raises(InvalidPostContent):
            create_post(
                user_id, 
                post_content
            )
            
        # Assert
     
        
@pytest.mark.django_db
@freeze_time("2020-04-18")
class TestCreateComments:
    
    pytestmark = pytest.mark.django_db
    
    def test_create_comment_with_valid_details_return_comment_id(
        self, user, post):
        
        # Arrange
        user_id = 2
        post_id = 1
        comment_content = "superb"
        
        # Act
        comment_id = create_comment(
            user_id, 
            post_id, 
            comment_content
        )
        
        # Assert
        comment = Comment.objects.get(
            id = comment_id
        )
        
        assert comment.content == comment_content
        assert comment.commented_by_id == user_id
        assert comment.post_id == post_id
        assert comment.commented_at == timezone.now()
        
    
    def test_create_comment_with_invalid_user_id_raise_error(
        self, post, user):
       
        # Arrange
        user_id = 0
        post_id = 2
        comment_content = "nice"
        
        # Act
        with pytest.raises(InvalidUserException):
            create_comment(
                user_id, 
                post_id, 
                comment_content
            )
            
        # Assert
        
        
    def test_create_comment_with_invalid_post_id_raise_error(
        self, post, user):
        
        # Arrange
        user_id = 1
        post_id = 0
        comment_content = "nice"
        
        # Act
        with pytest.raises(InvalidPostException):
            create_comment(
                user_id, 
                post_id, 
                comment_content
            )
            
        # Assert
        
        
    def test_create_comment_with_invalid_comment_content_raise_error(
        self, post, user):
        
        # Arrange
        user_id = 1
        post_id = 2
        comment_content = ""
        
        # Act
        with pytest.raises(InvalidCommentContent):
            create_comment(
                user_id, 
                post_id, 
                comment_content
            )
            
        # Assert
        
        
@pytest.mark.django_db
@freeze_time("2020-04-19")
class TestReplyToComment:
    
    pytestmark = pytest.mark.django_db
    
    def test_reply_to_comment_with_valid_details_return_comment_id(
        self, user, post, comment):
        
        # Arrange
        user_id = 2
        comment_id = 3
        reply_comment_content = "thanks"
        post_id = 2
        
        
        # Act
        comment_id2 = reply_to_comment(
            user_id, 
            comment_id, 
            reply_comment_content
        )
        
        
        # Assert
        comment = Comment.objects.get(
            id = comment_id2
        )
        
        assert comment.commented_by_id == user_id
        assert comment.content == reply_comment_content
        assert comment.parent_comment_id == comment_id
        assert comment.post_id == post_id
        assert comment.commented_at == timezone.now()
        
    
    def test_reply_to_reply_comment_with_valid_details_return_comment_id(
        self, user, post, comment, replycomment):
        
        # Arrange
        user_id = 2
        comments = Comment.objects.get(
            id = 4, 
            parent_comment_id = 1
        )
        comment_id = comments.id
        reply_comment_content = "hahaa"
        post_id = 1
        
        # Act
        comment_id2 = reply_to_comment(
            user_id, 
            comment_id, 
            reply_comment_content
        )
        
        # Assert
        comment = Comment.objects.get(
            id = comment_id2
        )
        
        assert comment.commented_by_id == user_id
        assert comment.content == reply_comment_content
        assert comment.parent_comment_id == comments.parent_comment_id
        assert comment.post_id == post_id
        assert comment.commented_at == timezone.now()
        
    
        
    def test_reply_to_comment_with_invalid_user_id_raise_error(
        self, user, post, comment):
        
        # Arrange
        user_id = 0
        comment_id = 1
        reply_comment_content = "thanks"
        
        # Act
        with pytest.raises(InvalidUserException):
            reply_to_comment(
                user_id, 
                comment_id, 
                reply_comment_content
            )
            
        # Assert
        
    def test_create_reply_to_comment_with_invalid_comment_id_raise_error(
        self, user, post, comment):
        
        # Arrange
        user_id = 1
        comment_id = 0
        reply_comment_content = "thanks"
        
        # Act
        with pytest.raises(InvalidCommentException):
            reply_to_comment(
                user_id, 
                comment_id, 
                reply_comment_content
            )
            
        # Assert
        
    def test_reply_to_comment_with_invalid_reply_comment_content_raise_error(
        self, user, post, comment):
       
        # Arrange
        user_id = 1
        comment_id = 1
        reply_comment_content = ""
        
        # Act
        with pytest.raises(InvalidReplyContent):
            reply_to_comment(
                user_id, 
                comment_id, 
                reply_comment_content
            )
            
        # Assert
           
           
@pytest.mark.django_db
@freeze_time("2020-04-19")
class TestReactToPost:
    
    def test_react_to_post_with_valid_details_for_the_first_time_create_reaction(
        self, user, post): 
        
        # Arrange
        user_id = 3
        post_id = 1
        reaction_type = ReactionEnum.WOW.value
        comment_id = None
        
        # Act
        react_to_post(
            user_id, 
            post_id, 
            reaction_type
        )
        
        # Assert
        react = Reaction.objects.get(
            post_id = post_id, 
            reacted_by_id = user_id
        )
    
        assert react.reaction == reaction_type
        assert react.comment_id == comment_id
        assert react.reacted_at == timezone.now()
        
    def test_react_to_post_with_valid_details_when_user_reacting_with_post_with_same_reaction_and_delete_reaction(
        self, user, post, reactpost): 
        
        # Arrange
        user_id = 3
        post_id = 1
        reaction_type = ReactionEnum.WOW.value
        
        # Act
        react_to_post(
            user_id, 
            post_id, 
            reaction_type
        )
        
        # Assert
        with pytest.raises(Reaction.DoesNotExist):
            Reaction.objects.get(
                post_id = post_id, 
                reacted_by_id = user_id
            )
        
    
    @pytest.mark.parametrize(
        'reaction_type_1',
        [(ReactionEnum.ANGRY.value),(ReactionEnum.WOW.value)])
    def test_react_to_post_with_valid_details_when_user_reacting_with_post_with_different_reaction_and_update_reaction(
        self, user, post, reaction_type_1): 
        
        # Arrange
        user_id = 2
        post_id = 1
        reaction_type = reaction_type_1
        
        # Act
        react_to_post(
            user_id, 
            post_id, 
            reaction_type
        )

        
        # Assert
        react = Reaction.objects.get(
            post_id = post_id, 
            reacted_by_id = user_id
        )
        
        assert react.reaction == reaction_type
        
    def test_react_to_post_with_invaid_user_id_raise_error(
        self, user, post):
        
        # Arrange
        user_id = 0
        post_id = 1
        reaction_type = ReactionEnum.WOW.value
        
        # Act
        with pytest.raises(InvalidUserException):
            react_to_post(
                user_id, 
                post_id, 
                reaction_type
            )
        
    def test_react_to_post_with_invaid_post_id_raise_error(
        self, user, post):
        
        # Arrange
        user_id = 1
        post_id = 0
        reaction_type = ReactionEnum.WOW.value
        
        # Act
        with pytest.raises(InvalidPostException):
            react_to_post(
                user_id, 
                post_id, 
                reaction_type
            )
            
    def test_react_to_post_with_invaid_reaction_type_raise_error(
        self, user, post):
        
        # Arrange
        user_id = 1
        post_id = 2
        reaction_type = 'LIKE'  
        
        # Act
        with pytest.raises(InvalidReactionTypeException):
            react_to_post(
                user_id, 
                post_id, 
                reaction_type
            )
        

@pytest.mark.django_db
@freeze_time("2020-04-19")
class TestReactToComment:
    
    def test_react_to_comment_with_valid_details_for_the_first_time_create_reaction(
        self, user, post, comment): 
        
        # Arrange
        user_id = 1
        comment_id = 1
        reaction_type = ReactionEnum.THUMBSUP.value
        
        # Act
        react_to_comment(
            user_id, 
            comment_id, 
            reaction_type
        )
        
        # Assert
        react = Reaction.objects.get(
            comment_id = comment_id, 
            reacted_by_id = user_id
        )
        
        assert react.reaction == reaction_type
        assert react.reacted_at == timezone.now()
        

    def test_react_to_comment_with_valid_details_when_user_reacting_with_post_with_same_reaction_and_delete_reaction(
        self, user, post, comment): 
        
        # Arrange
        user_id = 1
        comment_id = 1
        reaction_type = ReactionEnum.THUMBSUP.value
        react_to_comment(
            user_id, 
            comment_id, 
            reaction_type
        )
        
        # Act
        react_to_comment(
            user_id, 
            comment_id, 
            reaction_type
        )
        
        # Assert
        with pytest.raises(Reaction.DoesNotExist):
            Reaction.objects.get(
                comment_id = comment_id, 
                reacted_by_id = user_id
            )
        

    
    @pytest.mark.parametrize(
        'reaction_type_1',
        [(ReactionEnum.ANGRY.value),(ReactionEnum.WOW.value)])
    def test_react_to_comment_with_valid_details_when_user_reacting_with_post_with_different_reaction_and_update_reaction(
        self, user, post, comment, reaction_type_1): 
        
        # Arrange
        user_id = 1
        comment_id = 1
        reaction_type = reaction_type_1
        
        # Act
        react_to_comment(
            user_id, 
            comment_id, 
            reaction_type
        )
        
        # Assert
        react = Reaction.objects.get(
            comment_id = comment_id, 
            reacted_by_id = user_id
        )
        
        assert react.reaction == reaction_type
        
    def test_react_to_comment_with_invaid_user_id_raise_error(
        self, user, post, comment):
        
        # Arrange
        user_id = 0
        comment_id = 1
        reaction_type = ReactionEnum.WOW.value
        
        # Act
        with pytest.raises(InvalidUserException):
            react_to_comment(
                user_id, 
                comment_id, 
                reaction_type
            )
        
    def test_react_to_comment_with_invaid_post_id_raise_error(
        self, user, post, comment):
        
        # Arrange
        user_id = 1
        comment_id = 0
        reaction_type = ReactionEnum.WOW.value
        
        # Act
        with pytest.raises(InvalidCommentException):
            react_to_comment(
                user_id, 
                comment_id, 
                reaction_type
            )
            
    def test_react_to_comment_with_invaid_reaction_type_raise_error(
        self, user, post, comment):
        
        # Arrange
        user_id = 1
        comment_id = 1
        reaction_type = 'LIKE'
        
        # Act
        with pytest.raises(InvalidReactionTypeException):
            react_to_comment(
                user_id, 
                comment_id, 
                reaction_type
            )
            

@pytest.mark.django_db
def test_reactions_count_and_return_count_of_reactions(
    user, post, comment, replycomment, reactcomment, reactpost):
    
    # Arrange
    reactions = {'count': 9}
    
    # Act
    reactions_count = get_total_reaction_count()

    # Assert
    assert reactions_count == reactions

 
@pytest.mark.django_db
def test_get_reaction_matrices_for_given_post(
    user, post, comment, replycomment, reactpost, reactcomment):
    
    # Arrange
    post_id = 1
    post_reactions = {ReactionEnum.LOVE.value: 1, ReactionEnum.THUMBSDOWN.value: 1, ReactionEnum.WOW.value: 1}
    
    # Act
    reactions = get_reaction_metrics(post_id)
    
    # Assert
    assert reactions == post_reactions
    
    
@pytest.mark.django_db
class TestDeletePost:
    
        pytestmark = pytest.mark.django_db
        
        def test_delete_post_with_valid_user_id_and_post_id(
            self, user, post):
            
            # Arrange
            user_id = 1
            post_id = 1
            
            # Act
            delete_post(user_id, post_id)
            
            # Assert
            with pytest.raises(Post.DoesNotExist):
                Post.objects.get(id = post_id)
                
        def test_delete_post_with_invalid_user_id_raise_error(
            self, user, post):
           
            # Arrange
            user_id = 0
            post_id = 1
            
            # Act
            with pytest.raises(InvalidUserException):
                delete_post(user_id, post_id)
            
            # Assert
            
        def test_delete_post_with_invalid_post_id_raise_error(
            self, user, post):
            
            # Arrange
            user_id = 1
            post_id = 0
            
            # Act
            with pytest.raises(InvalidPostException):
                delete_post(user_id, post_id)
            
            # Assert
            
        def test_delete_post_with_user_id_not_matches_post_id(
            self, user, post):
            
            # Arrange
            user_id = 1
            post_id = 2
            
            # Act
            with pytest.raises(UserCannotDeletePostException):
                delete_post(user_id, post_id)
            
            # Assert
            
            
@pytest.mark.django_db
def test_get_posts_with_more_postive_reactions_and_return_post_ids(
    user, post, reactpost):  # TODO: Handle all 3 db states
   
    # Arrange
    post_list = [1]
    
    # Act
    posts = get_posts_with_more_positive_reactions()
    
    # Assert
    assert posts == post_list
    

@pytest.mark.django_db
def test_get_posts_with_more_negative_reactions_return_empty_list(
    user, post):
    
    # Arrange
    Reaction(
            post_id = 1, 
            reaction = ReactionEnum.THUMBSDOWN.value, 
            reacted_by_id = 4
        )
    Reaction(
            post_id = 1, 
            reaction = ReactionEnum.ANGRY.value, 
            reacted_by_id = 3
        )
    post_list = []
    
    # Act
    posts = get_posts_with_more_positive_reactions()
    
    # Assert
    assert posts == post_list


@pytest.mark.django_db
def test_get_posts_with_positive_reactions_equals_to_negative_reactions_return_empty_list(
    user, post):
    
    # Arrange
    Reaction(
            post_id = 1, 
            reaction = ReactionEnum.THUMBSDOWN.value, 
            reacted_by_id = 4
        )
        
    post_list = []
    
    # Act
    posts = get_posts_with_more_positive_reactions()
    
    # Assert
    assert posts == post_list

@pytest.mark.django_db
class TestReactedPosts:
    
    pytest.mark.django_db
    
    def test_get_posts_with_reacted_by_given_user_id_and_return_post_ids(
        self, user, post, reactpost):
        
        # Arrange
        user_id = 3
        reacted_posts = [1, 2, 3]
        
        # Act
        posts = get_posts_reacted_by_user(user_id)
        
        # Assert
        assert posts == reacted_posts
        
    def test_get_posts_with_reacted_by_invalid_user_id_raise_error(
        self, user, post):
        
        # Arrange
        user_id = 0
        
        # Act
        with pytest.raises(InvalidUserException):
                get_posts_reacted_by_user(user_id)
                

@pytest.mark.django_db
class TestGetReactionsToPosts:
    
    pytest.mark.django_db
    
    def test_get_reactions_to_post_with_valid_post_id(
        self, user, post, reactpost):
        
        # Arrange
        post_id = 2
        reactions_list = [{'user_id': 1, 'name': 'Prathap', 'profile_pic': '', 'reaction': 'LOVE'},
                            {'user_id': 3, 'name': 'Rajesh', 'profile_pic': '', 'reaction': 'SAD'}]
                
        # Act
        list2 = get_reactions_to_post(post_id)
        
        # Assert
        assert list2 == reactions_list
     
        
    def test_get_reactions_to_post_with_invalid_post_id_raise_error(
        self, user, post, reactpost):
        
        # Arrange
        post_id = 0
        
        # Act
        with pytest.raises(InvalidPostException):
                get_reactions_to_post(post_id)

               
@pytest.mark.django_db
class TestRepliesForComment:
    
    pytest.mark.django_db
    
    def test_get_replies_for_comment_and_return_list_of_replies(
        self, user, post, comment, replycomment):
        
        # Arrange
        comment_id = 2
        list_of_replies = [{'comment_id': 5,
                            'commenter': {
                                  'user_id': 1, 
                                  'name': 'Prathap', 
                                  'profile_pic': ''
                                },
                            'commented_at': '2020-04-18 00:00:00.000000',
                            'comment_content': 'haa'
            }]
        
        # Act
        replies = get_replies_for_comment(comment_id)
        
        # Assert
        assert replies == list_of_replies
      
        
    def test_get_replies_for_comment_with_invalid_comment_id_raise_error(
        self, user, post, comment, replycomment):
        
        # Arrange
        comment_id = 0
        
        # Act
        with pytest.raises(InvalidCommentException):
            get_replies_for_comment(comment_id)    
         
          
def check_post_details(posts, post_details):
    
    assert posts['posted_by'] == post_details['posted_by']
    assert posts['reactions'] == post_details['reactions']
    assert posts['comments'] == post_details['comments']
    assert posts['comments_count'] == post_details['comments_count']
        
    assert posts == post_details
    
            
@pytest.mark.django_db
class TestPostDetails:
    
    pytest.mark.django_db
    
    def test_get_details_of_post_with_valid_post_id(
        self, user, post, comment, replycomment, reactpost, reactcomment):
        
        # Arrange
        post_id = 1
        post_details = {'post_id': 1,
                        'posted_by': {
                             'name': 'Prathap', 
                             'user_id': 1, 
                             'profile_pic': ''
                            },
                         'posted_at': '2020-04-18 00:00:00.000000',
                         'post_content': 'Good morning',
                         'reactions': {
                             'count': 3, 
                             'type': ['WOW', 'THUMBS-DOWN', 'LOVE']
                            },
                         'comments': [{
                            'comment_id': 1,
                            'commenter': {
                               'user_id': 2, 
                               'name': 'Sagaram', 
                               'profile_pic': ''
                            },
                           'commented_at': '2020-04-18 00:00:00.000000',
                           'comment_content': 'nice',
                           'reactions': {
                               'count': 1, 
                               'type': ['THUMBS-UP']
                            },
                           'replies_count': 1,
                           'replies': [{
                             'comment_id': 4,
                             'commenter': {
                                 'user_id': 1, 
                                 'name': 'Prathap', 
                                 'profile_pic': ''
                                },
                             'commented_at': '2020-04-18 00:00:00.000000',
                             'comment_content': 'thanks',
                             'reactions': {
                                 'count': 1, 
                                 'type': ['LIT']
                                }
                            }]
                            },
                          {'comment_id': 2,
                           'commenter': {
                               'user_id': 3, 
                               'name': 'Rajesh', 
                               'profile_pic': ''
                            },
                           'commented_at': '2020-04-18 00:00:00.000000',
                           'comment_content': 'ohh',
                           'reactions': {
                               'count': 0, 
                               'type': []
                            },
                           'replies_count': 1,
                           'replies': [{
                             'comment_id': 5,
                             'commenter': {
                                 'user_id': 1, 
                                 'name': 'Prathap', 
                                 'profile_pic': ''
                                },
                             'commented_at': '2020-04-18 00:00:00.000000',
                             'comment_content': 'haa',
                             'reactions': {
                                 'count': 0, 
                                 'type': []
                                }
                            }]
                        }],
                        'comments_count': 2
        }
        
        

        
        # Act
        posts = get_post(post_id)
        
        # Assert
        check_post_details(posts, post_details)
        
        
        
    def test_get_details_of_post_with_invalid_post_id_raise_error(self):
        
        # Arrange
        post_id = 1
            
        # Act
        with pytest.raises(InvalidPostException):
            get_reactions_to_post(post_id)
 
          
@pytest.mark.django_db
class TestUserPosts:
    
    pytest.mark.django_db
    
    def test_get_user_posts_details_with_valid_user_id(
        self, user, post, comment, replycomment, reactpost, reactcomment):
       
        # Arrange
        user_id = 2
        user_post_details = [{'post_id': 2,
                              'posted_by': {
                                  'name': 'Sagaram', 
                                  'user_id': 2, 
                                  'profile_pic': ''
                                },
                              'posted_at': '2020-04-18 00:00:00.000000',
                              'post_content': 'hello',
                              'reactions': {
                                  'count': 2, 
                                  'type': ['LOVE', 'SAD']
                                },
                              'comments': [{
                                'comment_id': 3,
                                'commenter': {
                                    'user_id': 1, 
                                    'name': 'Prathap', 
                                    'profile_pic': ''
                                    },
                                'commented_at': '2020-04-18 00:00:00.000000',
                                'comment_content': 'ahaa',
                                'reactions': {
                                    'count': 1, 
                                    'type': ['WOW']
                                    },
                                'replies_count': 0,
                                'replies': []
                              }],
                              'comments_count': 1
        }]
                              

        # Act
        post_details = get_user_posts(user_id)
        
        # Assert
        check_post_details(post_details[0],  user_post_details[0])
        
        
    def test_get_user_posts_details_with_valid_user_id_and_users_do_not_have_any_posts_return_empty_list(
        self, user, post, comment, replycomment, reactpost, reactcomment):
         
         # Arrange
        user_id = 3
        user_post_details = []
        
        # Act
        post_details = get_user_posts(user_id)
        
        # Assert
        assert post_details == user_post_details
        
    def test_get_user_posts_details_with_invalid_user_id_raise_error(self):
        
        # Arrange
        user_id = 1
        
        # Act
        with pytest.raises(InvalidUserException):
            get_user_posts(user_id)
            
