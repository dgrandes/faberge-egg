unit Vehicles;

interface

uses
SysUtils, customers, Typez;

type
vehicle = class

private
pID : integer;
pcusts : custarray;
pcq:integer;
pcp:customer;

  published
    property ID:integer read pID write pID;
    property custs : custarray read pcusts write pcusts;
    property cq: integer read pcq write pcq;
    property cp: customer read pcp write pcp;
    constructor Create(ID : integer;cp:customer; cust : custarray;cq:integer);

 end;

 vearray = array of vehicle;
 
implementation

constructor Vehicle.Create(ID: integer ;cp:customer; cust: custarray;cq:integer);
begin
    self.ID := ID;
    self.cp:=cp;
    self.custs := cust;
    self.cq :=cq;
end;

end.
