unit Vehicles;

interface

uses
SysUtils, Typez;

type
vehicle = class

private
pID : integer;
pcusts : custarray;

  published
    property ID:integer read pID write pID;
    property custs : custarray read pcusts write pcusts;
    constructor Create(ID : integer; cust : custarray);

 end;

 vearray = array of vehicle;
 
implementation

constructor Vehicle.Create(ID: integer ; cust: custarray);
begin
    self.ID := ID;
    self.custs := cust;
end;

end.