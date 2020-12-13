pragma solidity ^0.4.24;
// We have to specify what version of compiler this code will compile with

contract Insepection {
  
  address private _admin;
  uint private _state;
    
  modifier onlyAdmin(){
        require(msg.sender == _admin, "you are not admin");
        _;
    }
  
  event setState(uint value);
  
  struct Product {
        uint id ;
        uint product_time ;
        uint transport_time ;
        uint inspection_time ;
        uint state;
        uint inspection_confidence ;
        uint Winners ;
        address add;
        string result;
    }


  mapping (bytes32 => uint8) public votesReceived;

  bytes32[] public propertyList;

  constructor(bytes32[] propertyNames) public {
    propertyList = propertyNames;
  }

  function getList() public view returns (bytes32[]) {
    return propertyList;
  }
 
  mapping (uint => Product) products;


 
 function setProduct(uint product_id,uint pt,uint tt) public{
     Product storage P = products[product_id];
     P.product_time = pt;
     P.transport_time = tt;
     P.add = msg.sender;
 }
 function getinformation(uint product_id) public view returns(uint pt,uint tt,uint it,address a,uint wi,uint s,string r){
          Product storage P = products[product_id];
          pt = P.product_time;
          tt = P.transport_time;
          it = P.inspection_time;
          s = P.state;
          r = P.result;
          wi = P.Winners;
          a = P.add;
          return (pt,tt,it,a,wi,s,r);
     
 } 
 function initial(uint product_id) public{
  Product storage P = products[product_id];
  P.id =product_id;
  P.state = 0;
  P.inspection_confidence=0;
  
}
 function consensus(uint product_id, uint state,uint it, uint ins_con, uint inspector_id) public{
      Product storage P = products[product_id];
      if(P.inspection_confidence < ins_con){
      P.inspection_time =  it;
      P.Winners = inspector_id;
      P.inspection_confidence = ins_con;
      P.state = state;}
      if(P.state > 3){
      P.result= 'True';}
      else {P.result='False';}
}
}