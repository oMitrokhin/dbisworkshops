create or replace package P_User is
procedure delete_user (email in User_product.user_email%type);
procedure edit_user (email in "User".user_email%type, user_password in "User".user_password%type, information "User".user_information%type);
end P_User;