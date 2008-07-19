
! Matlab-like linspace()
Subroutine linspace(x,y,lin,n)
Integer n,i
Real(8) lin(n)
Real x,y

!write(6,*) "x",x,"y",y,"n",n  ! dbg

Do i=1,n-1
   lin(i)=x+(i-1)*(y-x)/(n-1)
End Do
lin(n)=y;
END Subroutine linspace

! An identical copy of the above, simply to demo in the python wrapping a
! different way to expose the API for instructional purposes.
Subroutine linspace2(x,y,lin,n)
Integer n,i
Real(8) lin(n)
Real x,y

!write(6,*) "x",x,"y",y,"n",n  ! dbg

Do i=1,n-1
   lin(i)=x+(i-1)*(y-x)/(n-1)
End Do
lin(n)=y;
END Subroutine linspace2
