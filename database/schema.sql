create table customers (
  id varchar(20) primary key,
  name varchar(255) not null,
  email varchar(320) not null
);

create table tickets (
  id varchar(20) primary key,
  customer_id varchar(20) not null,
  title varchar(255) not null,
  description text not null,
  priority varchar(10) not null,
  status varchar(20) not null default 'open',

  constraint ticket_customer_fk
    foreign key (customer_id)
    references customers(id),

  constraint tickets_priority_check
    check (priority in ('low', 'medium', 'high')),

  constraint tickets_status_check
    check (status in ('open', 'in-progress', 'resolved'))
);