create or replace package body P_User is

procedure delete_user (email in User_product.user_email%type)
is
begin
delete from User_product
where user_email=email;
delete from "User"
where user_email=email;
end;
procedure edit_user (email in "User".user_email%type, user_password in "User".user_password%type, information "User".user_information%type)
is
begin
update "User"
    set user_password=user_password, user_information=information
where user_email = email;
end;

end;