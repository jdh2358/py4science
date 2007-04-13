C FILE: FIB3.F
      SUBROUTINE FIB(A,N)
C
C     CALCULATE FIRST N FIBONACCI NUMBERS
C
      INTEGER N
      REAL*8 A(N)
Cf2py intent(in) n
Cf2py intent(out) a
Cf2py depend(n) a
      DO I=1,N
         IF (I.EQ.1) THEN
            A(I) = 0.0D0
         ELSEIF (I.EQ.2) THEN
            A(I) = 1.0D0
         ELSE 
            A(I) = A(I-1) + A(I-2)
         ENDIF
      ENDDO
      END

      SUBROUTINE CUMSUM(X, Y, N)
C
C     COMPUTE THE CUMULATIVE SUM OF X
C
      INTEGER N
      REAL*8 X(N)
      REAL*8 Y(N)
Cf2py intent(in) x
Cf2py intent(out) y
Cf2py integer intent(hide),depend(X) :: n=len(x) 
      DO I=1,N
         IF (I.EQ.1) THEN
            Y(I) = X(I)
         ELSE 
            Y(I) = X(I) + Y(I-1)
         ENDIF
      ENDDO
      END

C END FILE FIB3.F
