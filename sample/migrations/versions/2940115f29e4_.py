"""empty message

Revision ID: 2940115f29e4
Revises: e8dde2e31305
Create Date: 2016-11-02 10:23:07.909000

"""

# revision identifiers, used by Alembic.
revision = '2940115f29e4'
down_revision = 'e8dde2e31305'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('posts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('body', sa.String(), nullable=True),
    sa.Column('body_html', sa.String(), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_posts_created'), 'posts', ['created'], unique=False)
    op.create_table('comments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('body', sa.String(), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('post_id', sa.Integer(), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_comments_created'), 'comments', ['created'], unique=False)
    op.add_column(u'users', sa.Column('locale', sa.String(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column(u'users', 'locale')
    op.drop_index(op.f('ix_comments_created'), table_name='comments')
    op.drop_table('comments')
    op.drop_index(op.f('ix_posts_created'), table_name='posts')
    op.drop_table('posts')
    ### end Alembic commands ###
