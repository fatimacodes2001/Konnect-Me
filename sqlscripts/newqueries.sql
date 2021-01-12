select * from status where 
status.page_email in (
select page_email as email from profile_follows_page pa
where pa.regular_profile_email="zain@abc.com" )

union

select* from status where status.regular_profile_email in(
select  followed_profile_email as email from profile_follows_profile pr
where pr.follower_email = "zain@abc.com");



select * from status inner join profile_follows_profile pr
on status.regular_profile_email = pr.follower_email
where pr.follower_email="zain@abc.com"
union
select* from status inner join profile_follows_page pa
on status.page_email = pa.page_email
where pa.regular_profile_email = "zain@abc.com";



select page.email from
profile_follows_page pa inner join page
on page.email = pa.page_email
where pa.regular_profile_email="zain@abc.com"

union

select regular_profile.email from
profile_follows_profile pr inner join regular_profile
on regular_profile.email = pr.followed_profile_email
where pr.follower_email="zain@abc.com";


select count(*) as total_count from (
select * from
profile_follows_page pa inner join page p
on p.email = pa.page_email
where pa.page_email="ibm@abc.com"
union
select * from
page_follows_page pg inner join page p
on p.email = pg.followed_page_email
where pr.followed_page_email="ibm@abc.com"
) tb;

select email from page where email in
(select p2.followed_page_email from profile_follows_page p1 inner join
page_follows_page p2 on p1.page_email = p2.follower_email
where p1.regular_profile_email = "zain@abc.com"
union
select p2.page_email from profile_follows_profile p1 inner join
profile_follows_page p2 on p1.followed_profile_email = p2.regular_profile_email
where p1.follower_email = "zain@abc.com")
order by numFollowers





