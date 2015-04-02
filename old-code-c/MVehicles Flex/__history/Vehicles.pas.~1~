unit Vehicles;

interface

type
vehicle = class

private
pcapa : integer;
pID : integer;
pcurr_pos : integer;

  published
    property capa:integer read pcapa write pcapa;
    property ID:integer read pID write pID;
    property curr_pos : integer read pcurr_pos write pcurr_pos;
    constructor Create(ID : integer; capa : integer);

 end;

implementation

constructor Vehicle.Create(ID: integer ; capa: Integer);
begin
    self.ID := ID;
    self.capa:= capa;
    self.curr_pos := 0;
end;

end.
