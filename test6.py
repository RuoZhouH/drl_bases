# Definition for singly-linked list.
class ListNode(object):
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution(object):
    def addTwoNumbers(self, l1, l2):
        """
        :type l1: ListNode
        :type l2: ListNode
        :rtype: ListNode
        """
        a, b = l1.val, l2.val
        temp1, temp2 = l1.next, l2.next
        i, j = 1, 1
        while temp1 is not None:
            a += temp1.val * pow(10, i)
            temp1 = temp1.next
            i += 1
        while temp2 is not None:
            b += temp2.val * pow(10, j)
            temp2 = temp2.next
            j += 1

        res = a + b

        ln = ListNode(res % 10, None)
        res = res // 10
        while res:
            node = ListNode(res % 10, None)
            cur = ln
            while cur.next != None:
                cur = cur.next
            cur.next = node
            res = res // 10
        return ln


l1 = ListNode(2, ListNode(4, ListNode(3, None)))
l2 = ListNode(5, ListNode(6, ListNode(4, None)))

res = Solution().addTwoNumbers(l1, l2)

print(res)
