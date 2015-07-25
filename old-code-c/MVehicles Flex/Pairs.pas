unit Pairs;

{$MODE Delphi}

interface

uses
  Sysutils, Customers, Vehicles, Math;

  type
  Pair = Class

  private
  pID:integer;
  pve : vearray;
  pline: customer;

  public
    constructor Create(ID:integer; ve:vearray; line:customer);
    property ID: integer read pID write pID;
    property ve: vearray read pve write pve;
    property line: customer read pline write pline;

  End;

 parray = array of pair;

 Trio= Class

  private
  pve : vearray;
  pline : custarray;

  public
    constructor Create(ve:vearray; line:custarray);
    property ve: vearray read pve write pve;
    property line: custarray read pline write pline;

 End;

implementation

constructor Pair.Create(ID: Integer; ve: vearray; line: Customer);
begin
    self.ID := ID;
    self.ve:= ve;
    self.line:= line;
end;

constructor Trio.Create(ve: vearray; line: custarray);
begin
    self.ve:= ve;
    self.line:= line;
end;
end.
