from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_babel import _
from app import db
from flask_login import current_user, login_required
from app.usercenter import bp
from app.usercenter.forms import form_edit_profile, form_edit_role, form_edit_permission, form_edit_role_add_perm, form_edit_role_for_user, form_add_role
from app.models import User, Role, Roletopermission, Permission, Usertorole

@bp.route('/lobby', methods=['GET', 'POST'])
def lobby():
    userlist = db.session.query(User).all()
    rolelist = db.session.query(Role).all()
    permissionlist = db.session.query(Permission).all()
    Usertorolelist = db.session.query(Usertorole).all()
    Roletopermissionlist = db.session.query(Roletopermission).all()
    return render_template('usercenter/lobby.html',
                           title=_('User Management'),
                           userlist=userlist,
                           rolelist=rolelist,
                           permissionlist=permissionlist,
                           usertorolelist=Usertorolelist,
                           roletopermissionlist=Roletopermissionlist
                           )

@bp.route('/show_user/<user>', methods=['GET', 'POST'])
@bp.route('/show_user', defaults={'user':'ALL'}, methods=['GET', 'POST'])
def list_user(user):
    if user=='ALL':
        userlist = db.session.query(User).all()
    else:
        userlist = db.session.query(User).filter(User.username==user).all()
    if len(userlist) == 0:
        return redirect(url_for('usercenter.list_user', user='ALL'))

    #Usertorolelist = db.session.query(Usertorole).join(Role, Usertorole.role_id== Role.id).filter(Usertorolelist.userid==current_user.id).all()
    #Roletopermissionlist = db.session.query(Roletopermission).join(Usertorolelist, Usertorolelist.role_id==Roletopermission.role_id).all()
    return render_template('usercenter/show_user.html',
                           title=_('User Management'),
                           datalist = userlist)



@bp.route('/add_role', methods=['GET', 'POST'])
def add_role():
    form=form_add_role()
    if current_user.check_permission('usercenter_role_add'):
        if form.validate_on_submit():
            if db.session.query(Role).filter(Role.rolename==form.roletoadd.data).count() == 0:
                newrole = Role(rolename=form.roletoadd.data)
                db.session.add(newrole)
                db.session.commit()
                flash ('Role has been added!')
            else:
                flash ('Role already exists!')
        else:
            print(form.errors)
            return render_template('usercenter/add_role.html', form=form)
    else:
        flash ('You have no permission to add new roles')
    return redirect(url_for('usercenter.list_role'))

@bp.route('/show_role', methods=['GET', 'POST'])
def list_role():
    form=form_add_role()
    page = request.args.get('page', 1, type=int)
    rolelist = db.session.query(Role).outerjoin(Roletopermission, Roletopermission.role_id == Role.id).all()

    for entry in rolelist:
        print (entry.rolename)

    return render_template('usercenter/show_role.html',
                           title=_('Role Management'),
                           form=form,
                           datalist = rolelist)

@bp.route('/show_permission', methods=['GET', 'POST'])
def list_permission():
    permissionlist = db.session.query(Permission).join(Roletopermission, Roletopermission.role_id == Permission.id).all()
    return render_template('usercenter/show_permission.html', title=_('Permission Management'), datalist = permissionlist)

@bp.route('/edit_profile_remove_role/<username>/<role>', methods=['GET', 'POST'])
@login_required
def usermanagement_revoke_role(username, role):
    if current_user.is_authenticated:
        if current_user.check_permission('usercenter_user_edit') and username != None:
            if User.query.filter(User.username == username).count() == 1:
                usertoedit = username
                user = User.query.filter(User.username == usertoedit).first()
                db.session.query(Usertorole).filter(Usertorole.user_id==user.id).filter(Usertorole.role_id==role).delete()
                db.session.commit()
            else:
                flash("No legal user found")
                usertoedit = current_user.username
        else:
            usertoedit = current_user.username
            flash ('You are not allowed to change other user settings')
            return redirect(url_for('usercenter.usermanagement', username=user.username))
    return redirect(url_for('usercenter.usermanagement', username=user.username))

@bp.route('/edit_profile_remove_permission/<role>/<permission>', methods=['GET', 'POST'])
@login_required
def usermanagement_revoke_permission(role, permission):
    role = role.replace("%20"," ")
    if current_user.is_authenticated:
        if current_user.check_permission('usercenter_role_edit') and permission != None:
            if Role.query.filter(Role.rolename == role).count() == 1:
                roletoedit = Role.query.filter(Role.rolename == role).first()
                db.session.query(Roletopermission).filter(Roletopermission.role_id==roletoedit.id).filter(Roletopermission.permission_id==permission).delete()
                db.session.commit()
            else:
                flash("No legal Role found")
                return redirect(url_for('usercenter.rolemanagement', role=role))
        else:
            flash ('You are not allowed to change Role settings')
            return redirect(url_for('usercenter.rolemanagement', role=role))
    return redirect(url_for('usercenter.rolemanagement', role=role))

@bp.route('/edit_profile', defaults={'username': None}, methods=['GET', 'POST'])
@bp.route('/edit_profile/<username>', methods=['GET', 'POST'])
@login_required
def usermanagement(username):
    if current_user.is_authenticated:
        if current_user.check_permission('usercenter_user_edit') and username != None:
            if User.query.filter(User.username == username).count() == 1:
                usertoedit = username
            else:
                flash("No legal user found")
                usertoedit = current_user.username
        else:
            usertoedit = current_user.username
            flash ('You are not allowed to change other user settings')
            return redirect('usercenter.usermanagement', username=username)
        user = User.query.filter(User.username == usertoedit).first()
        roles = Role.query.all()
        form = form_edit_profile()
        form2 = form_edit_role_for_user()
        form2.role.choices=gamelist = [(g.id, g.rolename) for g in Role.query.all()]
        if form2.validate_on_submit():
            if db.session.query(Usertorole).filter(Usertorole.user_id == current_user.id).filter(Usertorole.role_id==form2.role.data).count() == 0:
                newrole = Usertorole(role_id = form2.role.data, user_id = user.id)
                db.session.add(newrole)
                db.session.commit()
        if form.validate_on_submit():
            if User.query.filter(User.username == form.username.data).count() == 0 and form.username.data!=user:
                if form.username.data == "":
                    flash("NO emptry username allowed")
                else:
                    user.username=form.username.data
                    flash('Username has been updated')

            user.email=form.email.data
            user.real_name=form.name.data
            db.session.commit()
            flash('User has been updated')
        return render_template('usercenter/edit_profile.html',
                               title=_('Edit User'),
                               form=form,
                               form2=form2,
                               user=user)


@bp.route('/edit_role', defaults={'role': None}, methods=['GET', 'POST'])
@bp.route('/edit_role/<role>', methods=['GET', 'POST'])
@login_required
def rolemanagement(role):
    if current_user.is_authenticated:
        if current_user.check_permission('usercenter_role_edit'):
            if role != None:
                role = role.replace("%20","+")
                print(role)
                if Role.query.filter(Role.rolename == role).count() == 1:
                    roletoedit = role
                else:
                    flash("No legal role found")
                    return redirect(url_for('usercenter.list_role'))
            else:
                return redirect(url_for('usercenter.lobby'))
        else:
            flash ('You are not allowed to change')
            return redirect(url_for('usercenter.lobby'))

        role = Role.query.filter(Role.rolename == roletoedit).first()
        form = form_edit_role()
        if form.validate_on_submit():
            if form.old_rolename.data != form.rolename.data:
                if Role.query.filter(Role.rolename == form.old_rolename.data).count() == 1:
                    role.rolename=form.rolename.data
                    db.session.commit()
                    flash('Rolename has been changed to '+form.rolename.data)
                    print(role.rolename)
                    return redirect(url_for('usercenter.rolemanagement', role=role.rolename))

                if Role.query.filter(Role.rolename == form.old_rolename.data).count() == 0:
                    newrole = Role(rolename=form.rolename.data)
                    db.session.add(newrole)
                    db.session.commit()
                    flash('Rolename '+form.rolename.data+' has been created ')
                    print(role.rolename)
                else:
                    flash('Rolename already exists')
        flash (roletoedit)
        permissionlist =db.session.query(Permission).all()

        form2=form_edit_role_add_perm()
        form2.permissiontoadd.choices= [(g.id, g.permissionname) for g in Permission.query.all()]
        if form2.validate_on_submit():
            if db.session.query(Roletopermission).filter(Roletopermission.permission_id ==form2.permissiontoadd.data).filter(Roletopermission.role_id == role.id).count() == 0:
                permissionid =db.session.query(Permission).filter(Permission.id == form2.permissiontoadd.data).first()
                NewRoletopermission=Roletopermission(role_id=role.id, permission_id=permissionid.id)
                db.session.add(NewRoletopermission)
                db.session.commit()
        #choicelist = [(g.id, g.permissionname) for g in db.session.query(Permission).all()]
        #print(choicelist)
        # form2.permissiontoadd.choices=choicelist

        return render_template('usercenter/edit_role.html',
                               title=_('Edit Role'),
                               form=form,
                               form2=form2,
                               role=role,
                               permissionlist=permissionlist
                               )

@bp.route('/edit_permission', defaults={'permission': None}, methods=['GET', 'POST'])
@bp.route('/edit_permission/<permission>', methods=['GET', 'POST'])
@login_required
def permissionmanagement(permission):
    form = form_edit_permission()
    if current_user.is_authenticated:
        if current_user.check_permission('usercenter_permission_add') and permission == 'add':
            return render_template('usercenter/add_permission.html',
                                   title=_('Add Permission'),
                                   form=form)
        elif current_user.check_permission('usercenter_permission_add') and permission != None:
            permission = permission.replace("%20","+")
            print(permission)
            if Permission.query.filter(Permission.permissionname == permission).count() == 1:
                permissiontoedit = permission
            else:
                flash("No legal permission found")
        else:
            flash ('You are not allowed to change permission settings')
            return redirect(url_for('usercenter.lobby'))
        form = form_edit_permission()
        permission = Permission.query.filter(Permission.permissionname == permission).first()
        print(form.permissionname.data, form.permissionaction.data)
        if form.validate_on_submit():
            # Add new one
            if Permission.query.filter(Permission.permissionname == permission.permissionname).count() == 0:
                newpermission = Permission(permissionname = form.permissionname.data, action = form.permissionaction.data)
                db.session.add(newpermission)
                db.session.commit()
                flash('Permission '+form.permissionname.data+' has been created')
            elif Permission.query.filter(Permission.permissionname == permission.permissionname).count() == 1:
                permission = Permission.query.filter(Permission.permissionname == permissiontoedit).first()
                permission.permissionname=form.permissionname.data
                permission.action=form.permissionaction.data
                flash('Permission has been updated')

            db.session.commit()
        return render_template('usercenter/edit_permission.html',
                               title=_('Edit Permission'),
                               form=form,
                               permission=permission)



@bp.route('/delete_permission/<permission>', methods=['GET', 'POST'])
def delete_permission(permission):
    permission = permission.replace("%20","+")
    if current_user.is_authenticated:
        if current_user.check_permission('usercenter_permission_edit') and permission != None:
            if Permission.query.filter(Permission.permissionname == permission).count() == 1:
                item =Permission.query.filter(Permission.permissionname == permission).first()
                #Permission.query.filter(Permission.permissionname == permission).delete()
                db.session.delete(item)
                db.session.commit()
        else:
            flash('You are not allowed to edit permissions')
            return redirect(url_for('usercenter.permissionmanagement'))
    else:
        return redirect(url_for('auth.login'))
    return redirect(url_for('usercenter.permissionmanagement'))

@bp.route('/deleteuser/<userid>', methods=['GET', 'POST'])
def delete_user(userid):
    if current_user.is_authenticated:
        if current_user.check_permission('delete_user'):
            db.session.query(User).filter(user_id==userid).delete()
            db.session.commit()
            flash ('User has been deleted')
            return redirect(url_for('usercenter.lobby'))
    return redirect(url_for('main.index'))
