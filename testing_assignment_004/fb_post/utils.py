from . models import *
from . exceptions import *
from datetime import datetime

# Task-2
def create_post(user_id, post_content):
    user = User.objects.filter(id=user_id).exists()
    if not user:
        raise InvalidUserException
    if not post_content:
        raise InvalidPostContent
    else:
        post=Post.objects.create(
            content=post_content,
            posted_by_id=user_id
            )
        return post.id
  
# Task-3          
def create_comment(user_id, post_id, comment_content):
    user = User.objects.filter(id=user_id).exists()
    post = Post.objects.filter(id=post_id).exists()
    if not user:
        raise InvalidUserException
    if not post:
        raise InvalidPostException
    if not comment_content:
        raise InvalidCommentContent
    else:
        comment=Comment.objects.create(
            content=comment_content,
            commented_by_id=user_id,
            post_id=post_id
            )
        return comment.id
        
# Task-4
def reply_to_comment(user_id, comment_id, reply_content):
    user = User.objects.filter(id=user_id)
    comments = Comment.objects.filter(id=comment_id)
    len(comments)
    if not user:
        raise InvalidUserException
    if not comments:
        raise InvalidCommentException
    if not reply_content:
        raise InvalidReplyContent
    else:
        if(comments[0].parent_comment_id):
            comment=Comment.objects.create(
                content=reply_content,
                commented_by_id=user_id,
                post_id=comments[0].post_id,
                parent_comment_id=comments[0].parent_comment_id
                )
        else:
            comment=Comment.objects.create(
                content=reply_content,
                commented_by_id=user_id,
                post_id=comments[0].post_id,
                parent_comment_id=comment_id
                )
        return comment.id
        
# Task-5
def react_to_post(user_id, post_id, reaction_type):
    user = User.objects.filter(id=user_id)
    post = Post.objects.filter(id=post_id)
    if not user:
        raise InvalidUserException
    if not post:
        raise InvalidPostException
    if reaction_type not in ['WOW', 'LIT', 'LOVE', 'HAHA', 'THUMBS-UP',
                            'THUMBS-DOWN', 'ANGRY', 'SAD']:
        raise InvalidReactionTypeException
    else:
        try:
            react=Reaction.objects.get(
                reacted_by_id=user_id,
                post_id=post_id
            )
        except:
            Reaction.objects.create(
                reacted_by_id=user_id,
                post_id=post_id,
                reaction=reaction_type
            )
            return
            
        if react.reaction == reaction_type:
            react.delete()
        else:
            react.reaction = reaction_type
            react.reacted_at = datetime.now()
            react.save()
            
# Task-6
def react_to_comment(user_id, comment_id, reaction_type):
    user = User.objects.filter(id=user_id)
    comment = Comment.objects.filter(id=comment_id)
    if not user:
        raise InvalidUserException
    if not comment:
        raise InvalidCommentException
    if reaction_type not in ['WOW', 'LIT', 'LOVE', 'HAHA', 'THUMBS-UP',
                            'THUMBS-DOWN', 'ANGRY', 'SAD']:
        raise InvalidReactionTypeException
    else:
        try:
            react=Reaction.objects.get(
                reacted_by_id=user_id,
                comment_id=comment_id
                )
        except:
            Reaction.objects.create(
                reacted_by_id=user_id,
                comment_id=comment_id,
                reaction=reaction_type
                )
            return
            
        if react.reaction == reaction_type:
            react.delete()
        else:
            react.reaction = reaction_type
            react.reacted_at = datetime.now()
            react.save()
    
# Task-7
def get_total_reaction_count():
    return Reaction.objects.aggregate(
        count=Count('id')
        )
        
# Task-8
def get_reaction_metrics(post_id):
    post = Post.objects.filter(id=post_id)
    if not post:
        raise InvalidPostException
    else:
        matrices = Reaction.objects.values('reaction').filter(post_id=post_id).annotate(
            count=Count('reaction')
            )
        reaction_matrices={}
        for matric in  matrices:
            reaction_matrices[matric['reaction']] = matric['count']
    return reaction_matrices
    
# Task-9
def delete_post(user_id, post_id):
    post=Post.objects.filter(id=post_id,posted_by_id=user_id)
    if post:
        post.delete()
    else:
        #user = User.objects.filter(id=user_id).exists()
        #post = Post.objects.filter(id=post_id).exists()
        if not User.objects.filter(id=user_id).exists():
            raise InvalidUserException
        if not Post.objects.filter(id=post_id).exists():
            raise InvalidPostException
        raise UserCannotDeletePostException
        
# Task-10
def get_posts_with_more_positive_reactions():
    positive_reactions=[
        'THUMBS-UP', 'LIT', 'LOVE', 'HAHA', 'WOW'
        ]
    negative_reactions=[
        'SAD', 'ANGRY', 'THUMBS-DOWN'
        ]
    positive_count=Count('reactions',filter=Q(
        reactions__reaction__in=positive_reactions))
    negative_count=Count('reactions',filter=Q(
        reactions__reaction__in=negative_reactions))
    post=Post.objects.annotate(pcount=positive_count
        ).annotate(ncount=negative_count).filter(
        pcount__gt=F('ncount')
        ).values_list('id', flat=True)
    return list(post)
    
# Task-11
def get_posts_reacted_by_user(user_id):
    user = User.objects.filter(id=user_id)
    if not user:
        raise InvalidUserException
    else:
        post=Post.objects.filter(
            reactions__reacted_by_id=user_id
            ).values_list('id', flat=True)
        return list(post)
        
# Task-12
def get_reactions_to_post(post_id):
    post = Post.objects.filter(id=post_id)
    if not post:
        raise InvalidPostException
    else:
        reactions=Reaction.objects.filter(
            post_id=post_id
            ).select_related('reacted_by')
        user_list=[]
        for react in reactions:
            user_dict={
                'user_id': react.reacted_by_id,
                'name': react.reacted_by.name,
                'profile_pic': react.reacted_by.profile_pic,
                'reaction': react.reaction
            }
            user_list.append(user_dict)
        return user_list
        
# Task-13
def get_post(post_id,post_value=False):
    
    if not post_value:
        post = Post.objects.filter(id=post_id)
        
        if not post:
            raise InvalidPostException
            
        posts = Post.objects.filter(
                id=post_id).select_related(
                    'posted_by'
                    ).prefetch_related('reactions',
                    Prefetch('comments',
                    queryset=Comment.objects.select_related(
                        'commented_by').prefetch_related('reactions')))
        
    else:
        posts = Post.objects.filter(
            posted_by_id=post_id).select_related(
                'posted_by'
                ).prefetch_related('reactions',
                Prefetch('comments',
                queryset=Comment.objects.select_related(
                    'commented_by').prefetch_related('reactions')))
        """ 
            Post.objects.filter(
            posted_by_id=post_id).select_related(
                'posted_by'
                ).prefetch_related('reactions',
                'comments__commented_by',
                'comments__reactions')
                
        """
    
    post_list=[]
    
    for post in posts:
        comment_list=[]
            
        post_comments = list(post.comments.all())
        for comment in post_comments:
                
            if comment.parent_comment_id == None:
                    
                replies_list=[]
                comments_list=[]
                for comments in post_comments:
                    if comment.id == comments.parent_comment_id:
                        comments_list.append(comments)
                    
                for comment_reply in comments_list:
                        
                    reply_react_list=[]
                    for react in list(comment_reply.reactions.all()):
                        if react.reaction not in reply_react_list:
                            reply_react_list.append(react.reaction)
                        
                    replies_dict={
                            'comment_id': comment_reply.id,
                            'commenter': {
                                'user_id': comment_reply.commented_by_id,
                                'name': comment_reply.commented_by.name,
                                'profile_pic': comment_reply.commented_by.profile_pic
                            },
                            'commented_at': str(datetime.strftime(comment_reply.commented_at,'%Y-%m-%d %H:%M:%S.%f')),
                            'comment_content': comment_reply.content,
                            'reactions': {
                            'count': len(reply_react_list),
                            'type': reply_react_list
                            },
                    }
                    replies_list.append(replies_dict)
                        
                comment_react_list=[]
                for react in list(comment.reactions.all()):
                    if react.reaction not in comment_react_list:
                        comment_react_list.append(react.reaction)
                        
                comment_dict={
                        'comment_id': comment.id,
                        'commenter': {
                          'user_id': comment.commented_by_id,
                          'name': comment.commented_by.name,
                          'profile_pic': comment.commented_by.profile_pic
                        },
                        'commented_at': str(datetime.strftime(comment.commented_at,'%Y-%m-%d %H:%M:%S.%f')),
                        'comment_content': comment.content,
                        'reactions': {
                          'count': len(comment_react_list),
                          'type': comment_react_list
                        },
                        'replies_count': len(replies_list),
                        'replies': replies_list,
                }
                comment_list.append(comment_dict)
        post_react_list=[]
        for react in list(post.reactions.all()):
            if react.reaction not in post_react_list:
                post_react_list.append(react.reaction)
            
        post_dict={
                'post_id': post.id,
                'posted_by': {
                    'name': post.posted_by.name,
                    'user_id': post.posted_by_id,
                    'profile_pic': post.posted_by.profile_pic
                },
                'posted_at': str(datetime.strftime(post.posted_at,'%Y-%m-%d %H:%M:%S.%f')),
                'post_content': post.content,
                'reactions': {
                  'count': post.reactions.count(),
                  'type': post_react_list,
                },
                'comments': comment_list,
                'comments_count': len(comment_list),
        }
        post_list.append(post_dict)
    if post_value:
        return post_list
    else:
        return post_list[0]
# Task-14
def get_user_posts(user_id):
    user = User.objects.filter(id=user_id)
    if not user:
        raise InvalidUserException
    else:
        user_posts=get_post(user_id,post_value=True)
        return user_posts

# Task-15
def get_replies_for_comment(comment_id):
    comment = Comment.objects.filter(id=comment_id)
    if not comment:
        raise InvalidCommentException
    else:
        comments=Comment.objects.select_related(
            'commented_by').filter(
            parent_comment_id=comment_id
            )
            
        comment_list=[]
        for comment in comments:
            comment_dict={
                'comment_id': comment.id,
                'commenter': {
                  'user_id': comment.commented_by_id,
                  'name': comment.commented_by.name,
                  'profile_pic': comment.commented_by.profile_pic
                },
                'commented_at': str(datetime.strftime(comment.commented_at,'%Y-%m-%d %H:%M:%S.%f')),
                'comment_content': comment.content,
            }
            comment_list.append(comment_dict)
        return comment_list