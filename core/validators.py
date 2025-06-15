import re


class TCValidator:
    """Turkish Republic ID number validator."""
    
    @staticmethod
    def is_valid_tc(tc: str) -> bool:
        """Validate Turkish Republic ID number according to official algorithm."""
        if not re.fullmatch(r'\d{11}', tc):
            return False
            
        digits = list(map(int, tc))
        
        # First digit cannot be 0
        if digits[0] == 0:
            return False
            
        # Sum of first 10 digits mod 10 should equal 11th digit
        if sum(digits[:10]) % 10 != digits[10]:
            return False
            
        # Complex validation algorithm
        odd_sum = sum(digits[0:10:2])  # 1st, 3rd, 5th, 7th, 9th digits
        even_sum = sum(digits[1:9:2])  # 2nd, 4th, 6th, 8th digits
        
        if ((odd_sum * 7) - even_sum) % 10 != digits[9]:
            return False
            
        return True
    
    @staticmethod
    def extract_tc_from_text(text: str) -> str:
        """Extract valid TC number from text."""
        matches = re.findall(r'\b\d{11}\b', text)
        for match in matches:
            if TCValidator.is_valid_tc(match):
                return match
        return None


class VKNValidator:
    """Turkish Tax Number (VKN) validator."""
    
    @staticmethod
    def is_valid_vkn(vkn: str) -> bool:
        """Validate Turkish Tax Number according to official algorithm."""
        if not (vkn.isdigit() and len(vkn) == 10):
            return False

        digits = [int(d) for d in vkn]
        transformed = []

        # Transform each digit
        for i in range(9):
            tmp = (digits[i] + (9 - i)) % 10
            tmp = 10 if tmp == 0 else tmp
            transformed.append(tmp)

        # Calculate check digit
        total = 0
        for i in range(9):
            power = 2 ** (9 - i)
            total += (transformed[i] * power) % 9

        check_digit = (10 - (total % 10)) % 10
        return digits[9] == check_digit

    @staticmethod
    def extract_vkn_from_text(text: str) -> str:
        """Extract valid VKN number from text."""
        matches = re.findall(r'\b\d{10}\b', text)
        for match in matches:
            if VKNValidator.is_valid_vkn(match):
                return match
        return None


class DocumentIdentifier:
    """Main class for document identification number extraction."""
    
    @staticmethod
    def extract_identifier(text: str) -> str:
        """Extract TC or VKN from text, prioritizing TC."""
        # Try TC first
        tc = TCValidator.extract_tc_from_text(text)
        if tc:
            return tc
            
        # Try VKN if TC not found
        vkn = VKNValidator.extract_vkn_from_text(text)
        if vkn:
            return vkn
            
        return None
