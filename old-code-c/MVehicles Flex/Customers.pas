unit Customers;

{$MODE Delphi}

interface

uses SysUtils, Demands;

type
   Customer = Class

     private
     pID : Integer;
     pxcoor : real;
     pycoor : real;
     pdem : demand;

     public
     constructor Create(pID:integer; pxcoor, pycoor :real; pdem:demand);
     property ID : integer read pID write pID;
     property xcoor : real read pxcoor write pxcoor;
     property ycoor : real read pycoor write pycoor;
     property dem : demand read pdem write pdem;

                       
end;

custarray= array of customer;

   implementation
   constructor Customer.Create(pID: Integer; pxcoor: real; pycoor: real; pdem: demand);
   begin
          self.ID := pID;
          self.xcoor := pxcoor;
          self.ycoor := pycoor;
          self.dem := pdem;
   end;
end.
