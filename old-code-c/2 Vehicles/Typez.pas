unit Typez;

interface

uses
  SysUtils, Classes, Customers, Demands;

type
        CustArray = array of customer;
        realarray = array of array of real;
        rearray = array of real;
        intarray = array of integer;
        polar_coor =record
          cust:customer;
          ang:real;
        end;
        polararray = array of polar_coor;


var
  n:integer;
  Q: integer;
  dist:realarray;
  dep:customer;


implementation

end.