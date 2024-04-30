

Program RandomNetwork(input,netres);
{$M 16384,0,512000}

  Type
  ArcTreeType  = ^ArcRecord;
  ArcRecord    =
    RECORD
      ArcNumber:longint;
      ii :longint;
      jj :longint;
      cap:longint;
      LeftArcTree,RightArcTree:ArcTreeType;
    End;

  Var
    Arc:ArcTreeType;
    ArcTreeRoot:ArcTreeType;
    i,num,arcnumber:longint;
    num_arcs,num_nodes,capacity:longint;
    z:longint;
    X,Y:longint;
    xx1,xx2,xx3,xx4:longint;
    source,sink:longint;
    ch:char;
    found:boolean;
    found11,found22:boolean;
    OutFileName:string[20];
    netres:text;

  Function ArcTree(nn:longint):ArcTreeType;
    Var NewArc:ArcTreeType;
        nll,nrr:longint;
  Begin
    IF nn=0 THEN ArcTree:=nil ELSE
    Begin
      nll:=nn DIV 2; nrr:=nn-nll-1;
      xx1:=xx1+1;
      xx2:=0;xx3:=0;xx4:=0;
      NEW(NewArc);
      WITH NewArc^ DO
      Begin
        ArcNumber:=xx1;
        ii:=xx2; jj:=xx3; Cap:=xx4;
        LeftArcTree :=ArcTree(nll);
        RightArcTree:=ArcTree(nrr);
      End;
      ArcTree:=NewArc;
    End;
  End;

  Procedure LocateArc(t2:ArcTreeType; h2:longint);
    VAR Found2:BOOLEAN;
    Begin
      Found2:=FALSE;
      WHILE (t2<>nil) AND NOT Found2 DO
      Begin
        IF t2^.ArcNumber=h2 THEN Found2:=TRUE
        ELSE IF h2=t2^.LeftArcTree^.ArcNumber
        THEN t2:=t2^.LeftArcTree
        ELSE IF h2=t2^.RightArcTree^.ArcNumber
        THEN t2:=t2^.RightArcTree
        ELSE IF h2<t2^.RightArcTree^.ArcNumber
        THEN t2:=t2^.LeftArcTree
        ELSE IF h2>t2^.RightArcTree^.ArcNumber
        THEN t2:=t2^.RightArcTree;
      End;
      IF Found2 THEN Arc:=t2;
    End;

  Procedure PrintArcTree(ArcTree1:ArcTreeType);
    Begin
      IF ArcTree1<>nil THEN
      WITH ArcTree1^ DO
      Begin
        PrintArcTree(LeftArcTree);
        write(netres,'a');
        writeln(netres,ii:10,jj:10,Cap:10);
        z:=z+1;
        PrintArcTree(RightArcTree);
      End;
    End;

Procedure Randomnet;
  var complete:boolean;
  Procedure Add_Arc1;
    Begin
      z:=1;
      repeat
      Begin
        LocateArc(ArcTreeRoot,Z);
        IF (Arc^.ii=0) and (Arc^.jj=0) THEN
          Begin
            Arc^.ii:=X; Arc^.jj:=Y;
            Arc^.cap:=random(capacity)+1;
            IF z=num_arcs THEN complete:=true;
            z:=num_arcs;
          End;
        z:=z+1;
      End;
      until z=num_arcs+1;
    End;

  Procedure Add_Arc2;
    Begin
      z:=1;
      repeat
      Begin
        LocateArc(ArcTreeRoot,Z);
        IF (Arc^.ii=0) and (Arc^.jj=0) THEN
          Begin
            Arc^.ii:=Y; Arc^.jj:=X;
            Arc^.cap:=random(capacity)+1;
            IF z=num_arcs THEN complete:=true;
            z:=num_arcs;
          End;
        z:=z+1;
      End;
      until z=num_arcs+1;
    End;

  Begin
    complete:=false;
    repeat
    Begin
      Begin
        repeat
          X:=random(num_nodes)+1;
          Y:=random(num_nodes)+1;
        until (Y<>X);
      End;
      IF X<>Y THEN
      Begin
        found11:=false;
        found22:=false;
        for z:=1 to num_arcs do
        Begin
          LocateArc(ArcTreeRoot,Z);
          IF ((X=Arc^.ii) and (Y=Arc^.jj))
            THEN found11:=true;
        End;
        IF not found11 THEN Add_Arc1
        else if found11 then
        Begin
          for z:=1 to num_arcs do
          Begin
            LocateArc(ArcTreeRoot,Z);
            IF ((Y=Arc^.ii) and (X=Arc^.jj))
              THEN found22:=true;
          End;
          IF not found22 THEN Add_Arc2;
        End;
      End;
    End;
    until complete;
  End;
  
  Procedure Banner1;
    Begin
      writeln;
      writeln;
    End;

  Procedure Banner2;
    Begin
      writeln;
      writeln;
    End;

  Procedure Banner3;
    Begin
      writeln;
      writeln;
    End;

  Procedure Banner4;
    Begin
      writeln;
      writeln('  The network is completed. The data');
      writeln('  file is an ASCII file, and can be');
      writeln('  accessed with your editor. You may');
      writeln('  print the file using the DOS');
      writeln('  command PRINT ',OutFileName,'.max.');
    End;

  Procedure UserValues;
    var total_arcs:longint;
    Begin
      xx1:=0;
      repeat
        write('  How many nodes are in the network: ');
        readln(num_nodes);
        if (num_nodes<=1) then
        writeln('  Try again. Need at least two nodes.');
      until (num_nodes>1);
      total_arcs:=num_nodes*num_nodes-num_nodes;
      
      Begin
        repeat
          num_arcs:=num_nodes;
          if (num_arcs>total_arcs) OR (num_arcs<1) then
            Begin
              Banner2;
              writeln('  Try again with the number of');
              writeln('  arcs at least one, but not ');
              writeln('  more than ',total_arcs,'.');
              write('  How many arcs are in the network: ');
            End;
          until ((num_arcs<=total_arcs) AND (num_arcs>=1));
      End;      
      writeln('  What is the upper bound for arc flow');
      capacity:=50;
      source:=1;
      sink:=num_nodes;
      Banner3;
      writeln(netres,'c Random Network');
      writeln(netres,'c for Max-Flow');
      writeln(netres,'p max',num_nodes:10,num_arcs:10);
      writeln(netres,'n',source:14,'  s');
      writeln(netres,'n',sink:14,'  t');
      ArcTreeRoot:=ArcTree(num_arcs);
    End;

  Begin
    randomize;  {Turbo Pascal random number generator initiator.}
                {You may to replace this by compiler specific   }
                {randomizer, or write a short procedure.        }
    Banner1;
    
    ch:='y';
    if (ch='y') or (ch='Y') then
    Begin
      write('  Enter name of the output file: ');
      readln(OutFileName);
      assign(netres,OutFileName+'.max');
      rewrite(netres);
      UserValues;
      RandomNet;
      z:=1;
      PrintArcTree(ArcTreeRoot);
      close(netres);
      Banner4;
    End;
  End.