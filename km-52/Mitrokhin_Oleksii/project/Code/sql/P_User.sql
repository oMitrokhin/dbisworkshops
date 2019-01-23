create or replace package P_User is
type row_user is record(
user_email "User".user_email%type,
user_password "User".user_password%type,
user_information "User".user_information%type,
user_role "User".Role%type
);

Type tb_row_user is table of row_user;

function get_users_list
return tb_row_user
pipelined;

function get_user(email in "User".user_email%type)
return row_user;

function get_user_pass(email in "User".user_email%type)
return "User".user_password%type;

function get_user_email(email in "User".user_email%type)
return "User".user_email%type;

procedure block_un_user (email in User_product.user_email%type);
procedure delete_user (email in User_product.user_email%type);
procedure edit_user (email in "User".user_email%type, user_pass in "User".user_password%type, information in "User".user_information%type);
end P_User;
/
create or replace package body P_User is

function get_users_list
return tb_row_user
pipelined is
cursor user_list_curr is
select user_email,  user_password, user_information, role
from "User";
begin
for curr in user_list_curr
loop
    pipe row(curr);
end loop;
end get_users_list;

function get_user(email in "User".user_email%type)
return row_user
is
search_user row_user;
begin
    select * into search_user
    from "User"
    where user_email = email;
    
    if email!=search_user.user_email then
        return NULL;
    end if;
    return  search_user;
end get_user;

function get_user_pass(email in "User".user_email%type)
return "User".user_password%type
is
search_pass "User".user_password%type;
begin
    search_pass := NULL;
    select user_password into search_pass
    from "User"
    where user_email = email;
    if search_pass != NULL then
    return  search_pass;
    else 
    return NULL;
    end if;
end get_user_pass;

function get_user_email(email in "User".user_email%type)
return "User".user_email%type
is
search_email "User".user_email%type;
counter INTEGER;
begin
search_email := NULL;
    select count(*) into counter
    from "User"
    where user_email = email;
    if counter >0 then
      select email into search_email
    from "User"
    where user_email = email;
    return  search_email;
    else 
    return NULL;
    end if;
end get_user_email;

procedure block_un_user (email in User_product.user_email%type)
is
mail "User".user_email%type;
begin

select role into mail
from "User"
where user_email = email;
if mail in ('User') then

    update "User"
        set role='Banned'
    where user_email = email;
    commit;

else if mail in ('Banned') then
    update "User"
    set role='User'
    where user_email = email;
    commit;
end if;

end if;
end;

procedure delete_user (email in User_product.user_email%type)
is
begin
delete from User_product where user_email = email;
delete from "User" where user_email = email;
commit;
end;

procedure edit_user (email in "User".user_email%type, user_pass in "User".user_password%type, information in "User".user_information%type)
is
begin
update "User"
    set user_password=user_pass, user_information=information
where user_email = email;
commit;
end;

end P_User;