set serveroutput on

create or replace package User_auth as

procedure registration(email in "User".user_email%type, user_pass in "User".user_password%type, information "User".user_information%type);

function log_in(email in "User".user_email%type, user_pass in "User".user_password%type)
return "User".user_email%type;
end User_auth;

create or replace package  body user_auth as
    procedure registration(email in "User".user_email%type, user_pass in "User".user_password%type, information "User".user_information%type)
    is
    begin
        INSERT INTO "User"(user_email,role, user_password, user_information)
        values(email,'User', user_pass, information);
end registration;

function log_in(email in "User".user_email%type, user_pass in "User".user_password%type)
return "User".user_email%type
is
begin
    if email=P_User.get_user(email).user_email and user_pass=P_User.get_user(email).user_password then
    DBMS_OUTPUT.put_line('Log in done!');
    return email;
    else
    DBMS_OUTPUT.put_line('Invalid email or password');
    return Null;
    end if;
end log_in;
end User_auth;
    