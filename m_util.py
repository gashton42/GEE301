##    An adaption of Will McGugan's code for Beginning Game Development with Python and Pygame
##
##    Copyright 2007 Will McGugan
##
##    1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
##
##    2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
##
##    3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
##
##    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
##    PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
##    LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR
##    TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
##

from math import *

def format_number(n, accuracy=6):
    """Formats a number in a friendly manner
    (removes trailing zeros and unneccesary point."""

    fs = "%."+str(accuracy)+"f"
    str_n = fs%float(n)
    if '.' in str_n:
        str_n = str_n.rstrip('0').rstrip('.')
    if str_n == "-0":
        str_n = "0"
    #str_n = str_n.replace("-0", "0")
    return str_n


def lerp(a, b, i):
    """Linear enterpolate from a to b."""
    return a+(b-a)*i


def range2d(range_x, range_y):

    """Creates a 2D range."""

    range_x = list(range_x)
    return [ (x, y) for y in range_y for x in range_x ]


def xrange2d(range_x, range_y):

    """Iterates over a 2D range."""

    range_x = list(range_x)
    for y in range_y:
        for x in range_x:
            yield (x, y)


def saturate(value, low, high):
    return min(max(value, low), high)


def is_power_of_2(n):
    """Returns True if a value is a power of 2."""
    return log(n, 2) % 1.0 == 0.0


def next_power_of_2(n):
    """Returns the next power of 2 that is >= n"""
    return int(2 ** ceil(log(n, 2)))

if __name__ == "__main__":
    print("Import as a module to use properly")

##    print list( xrange2d(xrange(3), xrange(3)) )
##    print range2d(xrange(3), xrange(3))
##    print is_power_of_2(7)
##    print is_power_of_2(8)
##    print is_power_of_2(9)
##
##    print next_power_of_2(7)
