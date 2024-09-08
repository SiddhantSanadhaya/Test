
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.18;

contract RetailBilling {
    string public supermarketName = "Supermarket XYZ";
    uint256 public totalAmount = 0;
    uint256 public discountPercent = 5;
    uint256 public gstPercent = 7;
    uint256 public cgstPercent = 7;

    struct Item {
        string description;
        uint256 quantity;
        uint256 price;
        uint256 amount;
    }

    Item[] public items;

    // Event to log each purchase
    event ItemPurchased(string description, uint256 quantity, uint256 price, uint256 amount);

    // Function to add item purchased
    function addItem(string memory _description, uint256 _quantity, uint256 _price) public {
        uint256 itemAmount = _quantity * _price;
        totalAmount += itemAmount;

        items.push(Item({
            description: _description,
            quantity: _quantity,
            price: _price,
            amount: itemAmount
        }));

        emit ItemPurchased(_description, _quantity, _price, itemAmount);
    }

    // Function to print all items purchased
    function printItems() public view returns (string memory) {
        string memory result = string(abi.encodePacked(supermarketName, "\n"));
        result = string(abi.encodePacked(result, "Item Description | Quantity | Item Price | Amount\n"));

        for (uint i = 0; i < items.length; i++) {
            result = string(abi.encodePacked(
                result,
                items[i].description, " | ",
                uint2str(items[i].quantity), " | ",
                uint2str(items[i].price), " | ",
                uint2str(items[i].amount), "\n"
            ));
        }

        return result;
    }

    // Function to print total amount
    function printTotal(string memory _reason) public view returns (string memory) {
        return string(abi.encodePacked(_reason, ": ", uint2str(totalAmount), " wei\n"));
    }

    // Function to apply discount and print total after discount
    function applyDiscount() public view returns (string memory) {
        uint256 discountAmount = (totalAmount * discountPercent) / 100;
        uint256 discountedTotal = totalAmount - discountAmount;

        return string(abi.encodePacked(
            "Discount Amount: ", uint2str(discountAmount), " wei\n",
            "Total after discount: ", uint2str(discountedTotal), " wei\n"
        ));
    }

    // Function to calculate and apply tax, then print the final total
    function applyTax() public view returns (string memory) {
        uint256 discountedTotal = totalAmount - (totalAmount * discountPercent) / 100;
        uint256 gstAmount = (discountedTotal * gstPercent) / 100;
        uint256 cgstAmount = (discountedTotal * cgstPercent) / 100;
        uint256 finalAmount = discountedTotal + gstAmount + cgstAmount;

        return string(abi.encodePacked(
            "GST (7%): ", uint2str(gstAmount), " wei\n",
            "CGST (7%): ", uint2str(cgstAmount), " wei\n",
            "Final Total Amount: ", uint2str(finalAmount), " wei\n"
        ));
    }

    // Helper function to convert uint to string
    function uint2str(uint256 _i) internal pure returns (string memory _uintAsString) {
        if (_i == 0) {
            return "0";
        }
        uint256 j = _i;
        uint256 len;
        while (j != 0) {
            len++;
            j /= 10;
        }
        bytes memory bstr = new bytes(len);
        uint256 k = len;
        while (_i != 0) {
            k = k - 1;
            uint8 temp = (48 + uint8(_i - _i / 10 * 10));
            bytes1 b1 = bytes1(temp);
            bstr[k] = b1;
            _i /= 10;
        }
        return string(bstr);
    }
}